from flask import Blueprint

aulas_bp = Blueprint(name ='aulas', 
                    import_name= __name__, 
                    url_prefix='/aulas', 
                    template_folder='templates')

from .actions import routes