from datetime import datetime
from flask import render_template, session, redirect, url_for, current_app
from flask_login import login_required
from . import main
from .. import db    
from ..models import User
from ..email import send_email

@main.route('/')
def index():
    return render_template('main/index.html', current_time=datetime.utcnow())

@main.route('/user')
@login_required
def user():
    return render_template('main/user.html')