from flask import redirect, url_for,abort,session, request, flash, make_response
from urllib.parse import urlencode
from flask_login import current_user, login_user, logout_user
from ..api import SuapOAuth2
from ..database import db
from ..models.usuarios import User
from . import auth_bp
from .utils import create, cookies
import secrets, requests

#Atributos da API
suap_data = SuapOAuth2()

#Autorização
@auth_bp.route('/authorize/<provider>')
def oauth2_authorize(provider):
    if not current_user.is_anonymous:
        return redirect(url_for('index'))

    if suap_data is None:
        abort(404)

    # Gera um estado aleatório para o parâmetro state
    session['oauth2_state'] = secrets.token_urlsafe(16)

    # Cria uma string de consulta com todos os parâmetros do OAuth2
    qs = urlencode({
        'client_id': suap_data.SOCIAL_AUTH_SUAP_KEY,

        'redirect_uri': 'http://127.0.0.1:5000/auth/callback/suap',

        'response_type': 'code',
        'scope': 'email',
        'state': session['oauth2_state'],
    })

    # Redireciona o usuário para a URL de autorização do provedor OAuth2
    return redirect(suap_data.AUTHORIZATION_URL + '?' + qs)

#Confirmação
@auth_bp.route('/callback/<provider>')
def oauth2_callback(provider):
    if not current_user.is_anonymous:
        return redirect(url_for('index'))

    if suap_data is None:
        abort(404)

    if 'error' in request.args:
        for k, v in request.args.items():
            if k.startswith('error'):
                flash(f'{k}: {v}')
        return redirect(url_for('index'))

    if 'code' not in request.args:
        abort(401)

    response = requests.post(
        suap_data.ACCESS_TOKEN_URL,
        data={
            'client_id': suap_data.SOCIAL_AUTH_SUAP_KEY,
            'client_secret': suap_data.SOCIAL_AUTH_SUAP_SECRET,
            'code': request.args['code'],
            'grant_type': 'authorization_code',
            'redirect_uri': url_for('auth.oauth2_callback', provider=provider, _external=True),
        },
        headers={'Accept': 'application/json'}
    )

    oauth2_token = response.json().get('access_token')

    if not oauth2_token:
        abort(401)
        
    #Salvar Token na sessão
    session['access_token'] = oauth2_token

    user_response = requests.get(
        suap_data.USER_DATA_URL,
        headers={
            'Authorization': f'Bearer {oauth2_token}',
            'Accept': 'application/json',
        }
    )

    print(user_response.status_code)

    if response.status_code != 200:
        abort(401)

    user_infos = user_response.json()

    # Criar Usuário
    user = create.create_user(user_infos)
    #Login de Usuário
    login_user(user)

    #Cookies do usuário
    return cookies.set_cookies(user_infos)

#Logout de Usuário
@auth_bp.route('/logout/<provider>', methods=['POST'])
def logout(provider):
    if current_user.is_authenticated:
        # Obtém o token salvo na sessão
        oauth2_token = session.get('access_token')

        if oauth2_token:
            # Faz a requisição para revogar o token no SUAP
            response = requests.post(suap_data.REVOKE_TOKEN_URL, data={
                "token": oauth2_token,
                "client_id": suap_data.SOCIAL_AUTH_SUAP_KEY,
                "client_secret": suap_data.SOCIAL_AUTH_SUAP_SECRET,
            }, headers={'Accept': 'application/json'})

            if response.status_code == 200:
                # Remove o token da sessão
                session.pop("access_token", None)

        #Desloga o usuário do Flask-Login e apaga os cookies
        logout_user()
        resp = make_response(redirect(url_for('index')))
        cookies.delete_cookies(resp)
    return resp