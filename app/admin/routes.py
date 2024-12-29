from flask import render_template, flash, redirect, url_for, request
from flask_login import login_required, current_user
from functools import wraps
from app.admin import bp
from app.models import User, WardrobeItem
from app import db
from flask_wtf import FlaskForm
from wtforms import SubmitField

class EmptyForm(FlaskForm):
    submit = SubmitField('Submit')

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin:
            flash('You do not have permission to access this page.', 'error')
            return redirect(url_for('main.index'))
        return f(*args, **kwargs)
    return decorated_function

@bp.route('/dashboard')
@login_required
@admin_required
def admin_dashboard():
    total_users = User.query.count()
    total_items = WardrobeItem.query.count()
    recent_users = User.query.order_by(User.created_at.desc()).limit(5).all()
    recent_items = WardrobeItem.query.order_by(WardrobeItem.created_at.desc()).limit(5).all()
    
    return render_template('admin/dashboard.html',
                         title='Admin Dashboard',
                         total_users=total_users,
                         total_items=total_items,
                         recent_users=recent_users,
                         recent_items=recent_items)

@bp.route('/users')
@login_required
@admin_required
def manage_users():
    page = request.args.get('page', 1, type=int)
    users = User.query.paginate(page=page, per_page=20)
    form = EmptyForm()  # For CSRF protection
    return render_template('admin/users.html', title='Manage Users', users=users, form=form)

@bp.route('/items')
@login_required
@admin_required
def manage_items():
    page = request.args.get('page', 1, type=int)
    items = WardrobeItem.query.paginate(page=page, per_page=20)
    return render_template('admin/items.html', title='Manage Items', items=items)

@bp.route('/user/<int:id>/toggle-admin', methods=['POST'])
@login_required
@admin_required
def toggle_admin(id):
    form = EmptyForm()
    if not form.validate_on_submit():
        flash('Invalid request. Please try again.', 'error')
        return redirect(url_for('admin.manage_users'))
        
    user = User.query.get_or_404(id)
    if user == current_user:
        flash('You cannot modify your own admin status.', 'error')
    else:
        user.is_admin = not user.is_admin
        try:
            db.session.commit()
            flash(f'Admin status for {user.username} has been updated.', 'success')
        except Exception as e:
            db.session.rollback()
            flash('An error occurred while updating admin status.', 'error')
            
    return redirect(url_for('admin.manage_users'))

@bp.route('/item/<int:id>/delete', methods=['POST'])
@login_required
@admin_required
def delete_item(id):
    item = WardrobeItem.query.get_or_404(id)
    db.session.delete(item)
    db.session.commit()
    flash('Item has been deleted.', 'success')
    return redirect(url_for('admin.manage_items'))
