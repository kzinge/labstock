from ... import prof_bp
from flask import render_template, redirect, url_for
from ..services import user

@prof_bp.route('/laboratorios')
def labs():
    labs = user.get_labs()
    return render_template('viewlab.html', laboratorios = labs)

@prof_bp.route('/novareserva')
def novareserva():
    labs = user.get_labs()
    return render_template('novareserva.html', laboratorios = labs)