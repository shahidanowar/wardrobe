from flask import render_template, flash, redirect, url_for, request, jsonify
from flask_login import login_required, current_user
from app.main import bp
from app.models import WardrobeItem, Outfit
from app import db
from app.main.forms import ProfileForm, ChangePasswordForm

@bp.route('/')
@bp.route('/index')
@login_required
def index():
    return redirect(url_for('main.dashboard'))

@bp.route('/dashboard')
@login_required
def dashboard():
    # Get recent items
    recent_items = WardrobeItem.query.filter_by(user_id=current_user.id)\
        .order_by(WardrobeItem.created_at.desc()).limit(6).all()
    
    # Get recent outfits
    recent_outfits = Outfit.query.filter_by(user_id=current_user.id)\
        .order_by(Outfit.created_at.desc()).limit(5).all()
    
    return render_template('main/dashboard.html',
                         title='Dashboard',
                         recent_items=recent_items,
                         recent_outfits=recent_outfits)

@bp.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    form = ProfileForm()
    password_form = ChangePasswordForm()
    
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.email = form.email.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash('Your profile has been updated.', 'success')
        return redirect(url_for('main.profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
        form.about_me.data = current_user.about_me if hasattr(current_user, 'about_me') else ''
    
    return render_template('main/profile.html', 
                         title='Profile',
                         form=form,
                         password_form=password_form)

@bp.route('/change-password', methods=['POST'])
@login_required
def change_password():
    form = ChangePasswordForm()
    if form.validate_on_submit():
        if current_user.check_password(form.current_password.data):
            current_user.set_password(form.new_password.data)
            db.session.commit()
            flash('Your password has been updated.', 'success')
            return redirect(url_for('main.profile'))
        else:
            flash('Invalid current password.', 'danger')
    return redirect(url_for('main.profile'))
