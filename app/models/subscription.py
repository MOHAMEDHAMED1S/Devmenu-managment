from app import db
from datetime import datetime, timedelta

class Subscription(db.Model):
    __tablename__ = 'subscriptions'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    restaurant_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    website_url = db.Column(db.String(200))
    website_username = db.Column(db.String(100))
    website_password = db.Column(db.String(100))
    subscription_price = db.Column(db.Float, nullable=False)
    subscription_term = db.Column(db.String(20), nullable=False)  # monthly, quarterly, yearly
    payment_method = db.Column(db.String(50), nullable=False)
    status = db.Column(db.String(20), default='active')  # active, expired, paused
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    expires_at = db.Column(db.DateTime)
    paused_at = db.Column(db.DateTime)
    remaining_days = db.Column(db.Integer)
    
    # Relationships
    payments = db.relationship('Payment', backref='subscription', lazy=True)
    
    def __init__(self, **kwargs):
        super(Subscription, self).__init__(**kwargs)
        # Don't set expiration date here, it will be set in before_insert

    def update_expiration_date(self):
        if self.created_at is None:
            self.created_at = datetime.utcnow()
            
        if self.subscription_term == 'monthly':
            self.expires_at = self.created_at + timedelta(days=30)
        elif self.subscription_term == 'quarterly':
            self.expires_at = self.created_at + timedelta(days=90)
        elif self.subscription_term == 'yearly':
            self.expires_at = self.created_at + timedelta(days=365)
        self.remaining_days = (self.expires_at - datetime.utcnow()).days

    def update_status(self):
        if self.status == 'paused':
            return
            
        if datetime.utcnow() > self.expires_at:
            self.status = 'expired'
        else:
            self.status = 'active'
        self.remaining_days = (self.expires_at - datetime.utcnow()).days
        db.session.commit()

    def time_remaining(self):
        if self.status == 'paused':
            return 'Paused'
        elif self.status == 'expired':
            return 'Expired'
        else:
            days = (self.expires_at - datetime.utcnow()).days
            return f"{days} days"

    def pause(self):
        if self.status == 'active':
            self.status = 'paused'
            self.paused_at = datetime.utcnow()
            db.session.commit()
            return True
        return False

    def restart(self):
        if self.status == 'paused':
            # Calculate remaining time and add it to the current date
            remaining_time = self.expires_at - self.paused_at
            self.expires_at = datetime.utcnow() + remaining_time
            self.status = 'active'
            self.paused_at = None
            db.session.commit()
            return True
        return False
    
    def __repr__(self):
        return f'<Subscription {self.restaurant_name}>'

# Add event listeners to handle expiration date
@db.event.listens_for(Subscription, 'before_insert')
def set_expiration_date(mapper, connection, target):
    target.update_expiration_date()

@db.event.listens_for(Subscription, 'before_update')
def update_expiration_date_on_term_change(mapper, connection, target):
    if db.inspect(target).attrs.subscription_term.history.has_changes():
        target.update_expiration_date() 