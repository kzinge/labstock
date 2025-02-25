#Login com SUAP
from flask import Blueprint, redirect, url_for,abort,session, request, flash, make_response
from urllib.parse import urlencode

from flask_login import current_user, login_user, logout_user
from suap_beckend.beckend import SuapOAuth2
from database import db
from models.usuarios import User

import secrets, requests


auth_bp = Blueprint(name ='auth', 
                    import_name= __name__, 
                    url_prefix='/auth', 
                    template_folder='templates')

suap_data = SuapOAuth2()

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

        'redirect_uri': 'http://localhost:3000/auth/callback/suap',

        'response_type': 'code',
        'scope': 'email',
        'state': session['oauth2_state'],
    })

    # Redireciona o usuário para a URL de autorização do provedor OAuth2
    return redirect(suap_data.AUTHORIZATION_URL + '?' + qs)

#CALLBACK
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

    # Buscar usuário
    user = db.session.scalar(
        db.select(User).where(User.usu_matricula == user_infos['matricula'])
    )

    if user is None:
        
        if user_infos['tipo_vinculo'] == 'Servidor':

            if 'docente' in user_infos['vinculo']['categoria']:
                user = User(
                    nome= user_infos['nome_usual'],
                    email= user_infos['email'],
                    matricula= user_infos['matricula'],
                    tipo= 'Docente',
                    foto = user_infos['url_foto_75x100']
                    )
                db.session.add(user)
                db.session.commit()
            
            elif 'TECNICO' in user_infos['vinculo']['cargo']:
                user = User(
                    nome= user_infos['nome_usual'],
                    email= user_infos['email'],
                    matricula= user_infos['matricula'],
                    tipo= 'Técnico',
                    foto = user_infos['url_foto_75x100']
                    )
                db.session.add(user)
                db.session.commit()
        
        else:
            user = User(
                nome= user_infos['nome_usual'],
                email= user_infos['email'],
                matricula= user_infos['matricula'],
                tipo= user_infos['tipo_vinculo'],
                foto = user_infos['url_foto_75x100']
                )
            db.session.add(user)
            db.session.commit()


#Login de Usuário
    login_user(user)

    response_cookie = make_response(redirect(url_for('dashboard')))
    response_cookie.set_cookie('username', user_infos['nome_usual'], httponly=False)
    response_cookie.set_cookie('user_foto', user_infos['url_foto_75x100'], httponly=False)

    return response_cookie

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

        # Desloga o usuário do Flask-Login
        logout_user()
        resp = make_response(redirect(url_for('index'))) 
        resp.delete_cookie('username')
        resp.delete_cookie('user_foto')

    return resp