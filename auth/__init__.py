#Login com SUAP
#Rotas para materiais
from flask import Blueprint, render_template, redirect, url_for

auth_bp = Blueprint(name ='auth', 
                    import_name= __name__, 
                    url_prefix='/auth', 
                    template_folder='templates')
