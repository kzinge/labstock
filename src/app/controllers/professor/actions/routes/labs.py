from ... import prof_bp
from flask import render_template, redirect, url_for

@prof_bp.route('/reservas')
def reservas():
    return render_template('viewlab.html')