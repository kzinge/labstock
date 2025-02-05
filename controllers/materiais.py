#Rotas para materiais
from flask import Blueprint, render_template, redirect, url_for

materiais_bp = Blueprint(name ='material', 
                    import_name= __name__, 
                    url_prefix='/material', 
                    template_folder='templates')
