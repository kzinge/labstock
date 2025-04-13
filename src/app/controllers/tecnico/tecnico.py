#Rotas para técnicos
from flask import Blueprint, render_template, redirect, url_for
from flask_login import current_user
from ...database import db
from ...models import User

tec_bp = Blueprint(name ='tecnico', 
                    import_name= __name__, 
                    url_prefix='/tecnico', 
                    template_folder='pages')

@tec_bp.route('/')
def home():
    return 'teste'