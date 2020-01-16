from datetime import datetime
from flask import render_template, session, redirect, url_for, current_app
from flask_login import login_required
from . import main
from .. import db    
from ..models import User, Permission
from ..email import send_email
from ..decorators import admin_required, permission_required

@main.route('/')
def index():
    return render_template('main/index.html', current_time=datetime.utcnow())

@main.route('/user')
@login_required
def user():
    return render_template('main/user.html')

@main.route('/admin')
@login_required
@admin_required
def for_admins_only():
    return "For Administrators!"

@main.route('/moderate')
@login_required
@permission_required(Permission.MODERATE)
def for_moderators_only():
    return "For comment moderators!"