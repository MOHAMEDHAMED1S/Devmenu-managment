from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from app.models.user import User
from app.forms.auth import AdminLoginForm
from app import db

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard.index'))
    
    form = AdminLoginForm()
    if form.validate_on_submit():
        # Check if admin user exists
        admin = User.query.filter_by(email='mmop9909@gmail.com', is_admin=True).first()
        
        if not admin:
            # Create admin user if it doesn't exist
            admin = User(
                restaurant_name='Mohamed',
                email='mmop9909@gmail.com',
                is_admin=True
            )
            admin.set_password('Mohamedhamed')  # You should change this in production
            db.session.add(admin)
            db.session.commit()
        
        if admin.check_password(form.password.data):
            login_user(admin)
            next_page = request.args.get('next')
            return redirect(next_page or url_for('dashboard.index'))
        else:
            flash('Invalid password', 'danger')
    
    return render_template('auth/login.html', form=form)

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login')) 