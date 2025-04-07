from flask import Blueprint, render_template, jsonify, request, redirect, url_for
from flask_login import login_required, current_user
from app.models.subscription import Subscription
from app.models.payment import Payment
from datetime import datetime, timedelta
from sqlalchemy import func
from app import db

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/')
@login_required
def index():
    if not current_user.is_authenticated:
        return redirect(url_for('auth.login'))
    return render_template('dashboard/statistics.html')

@dashboard_bp.route('/api/statistics')
@login_required
def get_statistics():
    if not current_user.is_authenticated:
        return jsonify({'error': 'Unauthorized'}), 401
        
    # Get date range from request or default to current month
    year = int(request.args.get('year', datetime.utcnow().year))
    month = int(request.args.get('month', datetime.utcnow().month))
    
    start_date = datetime(year, month, 1)
    if month == 12:
        end_date = datetime(year + 1, 1, 1)
    else:
        end_date = datetime(year, month + 1, 1)
    
    # Calculate statistics
    total_revenue = db.session.query(func.sum(Payment.amount)).filter(
        Payment.payment_date >= start_date,
        Payment.payment_date < end_date,
        Payment.status == 'completed'
    ).scalar() or 0
    
    new_subscriptions = Subscription.query.filter(
        Subscription.created_at >= start_date,
        Subscription.created_at < end_date
    ).count()
    
    total_active = Subscription.query.filter(
        Subscription.status == 'active'
    ).count()
    
    expired_subscriptions = Subscription.query.filter(
        Subscription.updated_at >= start_date,
        Subscription.updated_at < end_date,
        Subscription.status == 'expired'
    ).count()
    
    churn_rate = (expired_subscriptions / total_active * 100) if total_active > 0 else 0
    
    return jsonify({
        'total_revenue': float(total_revenue),
        'new_subscriptions': new_subscriptions,
        'total_active': total_active,
        'churn_rate': round(churn_rate, 2),
        'period': f"{start_date.strftime('%B %Y')}"
    }) 