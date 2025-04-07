from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_required, current_user
from app.models.subscription import Subscription
from app.models.payment import Payment
from app import db
from datetime import datetime, timedelta
from app.forms.subscription import SubscriptionForm

subscription_bp = Blueprint('subscription', __name__)

@subscription_bp.route('/subscription/list')
@login_required
def list_subscriptions():
    if not current_user.is_authenticated:
        return redirect(url_for('auth.login'))
        
    subscriptions = Subscription.query.filter_by(user_id=current_user.id).all()
    return render_template('subscription/list.html', subscriptions=subscriptions)

@subscription_bp.route('/subscription/add', methods=['GET', 'POST'])
@login_required
def add_subscription():
    if not current_user.is_authenticated:
        return redirect(url_for('auth.login'))
        
    form = SubscriptionForm()
    if form.validate_on_submit():
        subscription = Subscription(
            user_id=current_user.id,
            restaurant_name=form.restaurant_name.data,
            email=form.email.data,
            website_url=form.website_url.data,
            website_username=form.website_username.data,
            website_password=form.website_password.data,
            subscription_price=form.subscription_price.data,
            subscription_term=form.subscription_term.data,
            payment_method=form.payment_method.data
        )
        db.session.add(subscription)
        db.session.commit()
        flash('Subscription added successfully!', 'success')
        return redirect(url_for('subscription.list_subscriptions'))
    
    return render_template('subscription/add.html', form=form)

@subscription_bp.route('/subscription/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def edit_subscription(id):
    if not current_user.is_authenticated:
        return redirect(url_for('auth.login'))
        
    subscription = Subscription.query.get_or_404(id)
    if subscription.user_id != current_user.id:
        flash('You do not have permission to edit this subscription.', 'danger')
        return redirect(url_for('subscription.list_subscriptions'))
        
    form = SubscriptionForm(obj=subscription)
    if form.validate_on_submit():
        subscription.restaurant_name = form.restaurant_name.data
        subscription.email = form.email.data
        subscription.website_url = form.website_url.data
        subscription.website_username = form.website_username.data
        subscription.website_password = form.website_password.data
        subscription.subscription_price = form.subscription_price.data
        subscription.subscription_term = form.subscription_term.data
        subscription.payment_method = form.payment_method.data
        db.session.commit()
        flash('Subscription updated successfully!', 'success')
        return redirect(url_for('subscription.list_subscriptions'))
    
    return render_template('subscription/add.html', form=form, subscription=subscription)

@subscription_bp.route('/subscription/<int:id>/delete', methods=['POST'])
@login_required
def delete_subscription(id):
    if not current_user.is_authenticated:
        return redirect(url_for('auth.login'))
        
    subscription = Subscription.query.get_or_404(id)
    if subscription.user_id != current_user.id:
        flash('You do not have permission to delete this subscription.', 'danger')
        return redirect(url_for('subscription.list_subscriptions'))
        
    db.session.delete(subscription)
    db.session.commit()
    flash('Subscription deleted successfully!', 'success')
    return redirect(url_for('subscription.list_subscriptions'))

@subscription_bp.route('/subscription/<int:id>/pause', methods=['POST'])
@login_required
def pause_subscription(id):
    if not current_user.is_authenticated:
        return redirect(url_for('auth.login'))
        
    subscription = Subscription.query.get_or_404(id)
    if subscription.user_id != current_user.id:
        return jsonify({'error': 'Unauthorized'}), 403
        
    if subscription.pause():
        return jsonify({'message': 'Subscription paused successfully'})
    return jsonify({'error': 'Subscription cannot be paused'}), 400

@subscription_bp.route('/subscription/<int:id>/restart', methods=['POST'])
@login_required
def restart_subscription(id):
    if not current_user.is_authenticated:
        return redirect(url_for('auth.login'))
        
    subscription = Subscription.query.get_or_404(id)
    if subscription.user_id != current_user.id:
        return jsonify({'error': 'Unauthorized'}), 403
        
    if subscription.restart():
        return jsonify({'message': 'Subscription restarted successfully'})
    return jsonify({'error': 'Subscription cannot be restarted'}), 400

@subscription_bp.route('/subscription/<int:id>/view')
@login_required
def view_subscription(id):
    if not current_user.is_authenticated:
        return redirect(url_for('auth.login'))
        
    subscription = Subscription.query.get_or_404(id)
    if subscription.user_id != current_user.id:
        flash('You do not have permission to view this subscription.', 'danger')
        return redirect(url_for('subscription.list_subscriptions'))
        
    return render_template('subscription/view.html', subscription=subscription)

@subscription_bp.route('/subscription/<int:id>/renew', methods=['POST'])
@login_required
def renew_subscription(id):
    subscription = Subscription.query.get_or_404(id)
    
    if subscription.user_id != current_user.id:
        flash('Unauthorized access', 'danger')
        return redirect(url_for('subscription.list_subscriptions'))
    
    try:
        term_months = int(request.form.get('term_months'))
        subscription.renew(term_months)
        
        # Create payment record for renewal
        payment = Payment(
            subscription_id=subscription.id,
            amount=subscription.price,
            payment_method=request.form.get('payment_method'),
            transaction_id=request.form.get('transaction_id'),
            status='completed'
        )
        
        db.session.add(payment)
        db.session.commit()
        
        flash('Subscription renewed successfully!', 'success')
    except Exception as e:
        db.session.rollback()
        flash('Error renewing subscription. Please try again.', 'danger')
    
    return redirect(url_for('subscription.list_subscriptions'))

@subscription_bp.route('/api/subscription/<int:id>/status')
@login_required
def get_subscription_status(id):
    subscription = Subscription.query.get_or_404(id)
    
    if subscription.user_id != current_user.id:
        return jsonify({'error': 'Unauthorized'}), 403
    
    subscription.update_status()
    return jsonify({
        'status': subscription.status,
        'time_remaining': subscription.time_remaining()
    }) 