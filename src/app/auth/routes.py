from flask import redirect, url_for, abort, session, request, flash, make_response, jsonify
from flask_login import current_user, login_user, logout_user
from urllib.parse import urlencode
from ..api import SuapOAuth2
from ..database import db
from ..models.usuarios import User
from . import auth_bp
from .utils import create, cookies
import secrets, requests

# Configuração SUAP
suap_data = SuapOAuth2()

# ------------------------
# Autorizar usuário
# ------------------------
@auth_bp.route('/authorize/<provider>')
def oauth2_authorize(provider):
    if not current_user.is_anonymous:
        return redirect(url_for('index'))

    if suap_data is None:
        abort(404)

    # Gera um estado aleatório
    session['oauth2_state'] = secrets.token_urlsafe(16)

    # URL de callback externa
    redirect_uri = url_for('auth.oauth2_callback', provider=provider, _external=True)

    # Parâmetros do OAuth2
    qs = urlencode({
        'client_id': suap_data.SOCIAL_AUTH_SUAP_KEY,
        'redirect_uri': redirect_uri,
        'response_type': 'code',
        'scope': 'email',
        'state': session['oauth2_state'],
    })

    # Redireciona para SUAP
    return redirect(f"{suap_data.AUTHORIZATION_URL}?{qs}")


# ------------------------
# Callback do SUAP
# ------------------------
@auth_bp.route('/callback/<provider>')
def oauth2_callback(provider):
    if not current_user.is_anonymous:
        return redirect(url_for('index'))

    if suap_data is None:
        abort(404)

    # Tratamento de erro do SUAP
    if 'error' in request.args:
        for k, v in request.args.items():
            if k.startswith('error'):
                flash(f'{k}: {v}')
        return redirect(url_for('index'))

    # Código OAuth
    code = request.args.get('code')
    if not code:
        abort(401)

    redirect_uri = url_for('auth.oauth2_callback', provider=provider, _external=True)

    # Troca código por token
    token_response = requests.post(
        suap_data.ACCESS_TOKEN_URL,
        data={
            'client_id': suap_data.SOCIAL_AUTH_SUAP_KEY,
            'client_secret': suap_data.SOCIAL_AUTH_SUAP_SECRET,
            'code': code,
            'grant_type': 'authorization_code',
            'redirect_uri': redirect_uri,
        },
        headers={'Accept': 'application/json'}
    )

    if token_response.status_code != 200:
        abort(401, description="Falha ao obter token do SUAP")

    oauth2_token = token_response.json().get('access_token')
    if not oauth2_token:
        abort(401, description="Token inválido")

    # Salvar token na sessão
    session['access_token'] = oauth2_token

    # Pegar dados do usuário
    user_response = requests.get(
        suap_data.USER_DATA_URL,
        headers={
            'Authorization': f'Bearer {oauth2_token}',
            'Accept': 'application/json'
        }
    )

    if user_response.status_code != 200:
        abort(401, description="Falha ao obter dados do usuário")

    user_infos = user_response.json()

    # Criar ou atualizar usuário
    user = create.create_user(user_infos)

    # Login do usuário
    login_user(user)

    # Setar cookies
    return cookies.set_cookies(user_infos)


# ------------------------
# Logout
# ------------------------
@auth_bp.route('/logout/<provider>', methods=['POST'])
def logout(provider):
    resp = make_response(redirect(url_for('index')))
    
    if current_user.is_authenticated:
        # Revogar token no SUAP
        oauth2_token = session.get('access_token')
        if oauth2_token:
            requests.post(
                suap_data.REVOKE_TOKEN_URL,
                data={
                    "token": oauth2_token,
                    "client_id": suap_data.SOCIAL_AUTH_SUAP_KEY,
                    "client_secret": suap_data.SOCIAL_AUTH_SUAP_SECRET,
                },
                headers={'Accept': 'application/json'}
            )
            session.pop("access_token", None)

        # Logout Flask-Login e apagar cookies
        logout_user()
        cookies.delete_cookies(resp)

    return resp
