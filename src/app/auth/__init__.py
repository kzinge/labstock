#Login com SUAP
from flask import Blueprint

auth_bp = Blueprint(name ='auth', 
                    import_name= __name__, 
                    url_prefix='/auth', 
                    template_folder='templates')
#Rotas
from . import routes