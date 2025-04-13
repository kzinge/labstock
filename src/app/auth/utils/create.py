from ...database import db
from ...models.usuarios import User

def create_user(user_infos):
    user = db.session.scalar(
        db.select(User).where(User.usu_matricula == user_infos['matricula'])
    )

    if user is None:
        if user_infos['tipo_vinculo'] == 'Servidor':
            if 'docente' in user_infos['vinculo']['categoria']:
                tipo = 'Docente'
            elif 'TECNICO' in user_infos['vinculo']['cargo']:
                tipo = 'Técnico'
            else:
                tipo = 'Servidor'
        elif user_infos['tipo_vinculo'] == 'Prestador de Serviço':
            tipo = 'Docente'
        else:
            tipo = user_infos['tipo_vinculo']

        user = User(
            nome=user_infos['nome_usual'],
            email=user_infos['email'],
            matricula=user_infos['matricula'],
            tipo=tipo,
            foto=user_infos['url_foto_75x100']
        )
        db.session.add(user)
        db.session.commit()
    return user