# core/views.py

from flask import render_template,request,Blueprint
from flask_security import current_user

core = Blueprint('core',__name__)

@core.route('/')
def index():
    #MORE TO COME!
    return render_template('index.html')
    #return render_template('index.html',current_user=current_user)

@core.route('/info')
def info():
    return render_template('info.html')
