#Login com SUAP
from flask import Blueprint, render_template, redirect, url_for,abort,session, request, flash, Flask
from urllib.parse import urlencode
from flask_login import current_user, LoginManager, login_user
from ..suap_beckend.beckend import SuapOAuth2
from ..database import db
from ..models.usuarios import User
import secrets
import requests 

auth_bp = Blueprint(name ='auth', 
                    import_name= __name__, 
                    url_prefix='/auth', 
                    template_folder='templates')


@auth_bp.route('/authorize/<provider>')
def oauth2_authorize(provider):
    if not current_user.is_anonymous:
        return redirect(url_for('index'))

    provider_data = SuapOAuth2()
    if provider_data is None:
        abort(404)

    # Gera um estado aleatório para o parâmetro state
    session['oauth2_state'] = secrets.token_urlsafe(16)

    # Cria uma string de consulta com todos os parâmetros do OAuth2
    qs = urlencode({
        'client_id': provider_data.SOCIAL_AUTH_SUAP_KEY,
        'redirect_uri': 'http://localhost:5000/callback/suap',
        'response_type': 'code',
        'scope': ' '.join(provider_data.USER_DATA_URL),
        'state': session['oauth2_state'],
    })

    # Redireciona o usuário para a URL de autorização do provedor OAuth2
    return redirect(provider_data.AUTHORIZATION_URL + '?' + qs)

#CALLBACK
@auth_bp.route('/callback/<provider>')
def oauth2_callback(provider):
    if not current_user.is_anonymous:
        return redirect(url_for('index'))

    provider_data = SuapOAuth2()
    if provider_data is None:
        abort(404)

    if 'error' in request.args:
        for k, v in request.args.items():
            if k.startswith('error'):
                flash(f'{k}: {v}')
        return redirect(url_for('index'))


    if request.args['state'] != session.get('oauth2_state'):
        abort(401)

    if 'code' not in request.args:
        abort(401)

    # token
    response = requests.post(provider_data.ACCESS_TOKEN_URL, data={
        'client_id': provider_data.SOCIAL_AUTH_SUAP_KEY,
        'client_secret': provider_data.SOCIAL_AUTH_SUAP_SECRET,
        'code': request.args['code'],
        'grant_type': 'authorization_code',
        'redirect_uri': url_for('oauth2_callback', provider=provider,
                                _external=True),
    }, headers={'Accept': 'application/json'})
    
    if response.status_code != 200:
        abort(401)
        
    oauth2_token = response.json().get('access_token')
    if not oauth2_token:
        abort(401)

    user_response = response.json().get(oauth2_token)

    if 'error' in user_response:
        abort(401)

    user_infos = provider_data.user_data(oauth2_token)

    #buscar user
    user = db.session.scalar(db.select(User).where(User.usu_email == user_infos['email']))

    if user is None:
        user = User(nome = user_infos['username'], email= user_infos['email'])
        db.session.add(user)
        db.session.commit()


    login_user(user)
    return redirect(url_for('index'))