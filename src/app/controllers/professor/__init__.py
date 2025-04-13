from flask import Blueprint

prof_bp = Blueprint(name ='professor', 
                    import_name= __name__, 
                    url_prefix='/professor', 
                    template_folder='views')

from .actions import routes