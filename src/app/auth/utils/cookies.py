from flask import make_response, redirect, url_for
# Nomes de cookies
COOKIE_USERNAME = 'username'
COOKIE_USER_FOTO = 'user_foto'
COOKIE_USERTYPE = 'usertype'

# Tipos de usuário
USER_TYPE_PROFESSOR = 'Professor'
USER_TYPE_TECNICO = 'Técnico'
USER_TYPE_ALUNO = 'Aluno'

def set_cookies(user_infos):
    response = make_response(redirect(url_for('dashboard')))
    response.set_cookie(COOKIE_USERNAME, user_infos['nome_usual'], httponly=False)
    response.set_cookie(COOKIE_USER_FOTO, user_infos['url_foto_75x100'], httponly=False)

    if user_infos['tipo_vinculo'] == 'Servidor':
        if 'docente' in user_infos['vinculo']['categoria']:
            response.set_cookie(COOKIE_USERTYPE, USER_TYPE_PROFESSOR, httponly=False)
        elif 'TECNICO' in user_infos['vinculo']['categoria']:
            response.set_cookie(COOKIE_USERTYPE, USER_TYPE_TECNICO, httponly=False)
    else:
        response.set_cookie(COOKIE_USERTYPE, USER_TYPE_ALUNO, httponly=False)

    return response

def delete_cookies(response):
    response.delete_cookie(COOKIE_USERNAME)
    response.delete_cookie(COOKIE_USER_FOTO)
    response.delete_cookie(COOKIE_USERTYPE)
    return response