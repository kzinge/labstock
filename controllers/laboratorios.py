#Rotas para laboratórios
from flask import Blueprint, render_template, redirect, url_for

lab_bp = Blueprint(name ='lab', 
                    import_name= __name__, 
                    url_prefix='/lab', 
                    template_folder='templates')

@lab_bp.route('/')
def index():
    return 'laboratorios'