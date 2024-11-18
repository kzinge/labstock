#Rotas para usuarios
from flask import Blueprint, render_template, redirect, url_for

usu_bp = Blueprint(name ='usuario', 
                    import_name= __name__, 
                    url_prefix='/usuario', 
                    template_folder='templates')
