from datetime import datetime
from flask import render_template, session, redirect, url_for, current_app, flash
from flask_login import login_required, current_user
from . import main
from .forms import EditProfileForm
from .. import db    
from ..models import User, Permission
from ..email import send_email
from ..decorators import admin_required, permission_required

@main.route('/')
def index():
    return render_template('main/index.html', current_time=datetime.utcnow())

@main.route('/user/<username>')
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    return render_template('main/user.html', user=user)

@main.route('/admin')
@login_required
@admin_required
def for_admins_only():
    return render_template('main/admin.html')
    
@main.route('/moderate')
@login_required
@permission_required(Permission.MODERATE)
def for_moderators_only():
    return "For comment moderators!"

@main.route('/edit-profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        current_user.name = form.name.data 
        current_user.location = form.location.data 
        current_user.about_me = form.about_me.data 
        db.session.add(current_user._get_current_object())
        db.session.commit()
        flash('Your profile has been updated.', 'dark')
        return redirect(url_for('.user', username=current_user.username))
    form.name.data = current_user.name 
    form.location.data = current_user.location 
    form.about_me.data = current_user.about_me 
    return render_template('main/edit_profile.html', form=form)
