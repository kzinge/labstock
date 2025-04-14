from flask import Blueprint

materiais_bp = Blueprint(name ='material',
                    import_name= __name__, 
                    url_prefix='/material', 
                    template_folder='templates')

from .actions import routes