from flask_login import UserMixin
from .. import db

class PaymentMethod(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    name = db.Column(db.String(1000))

    orders = db.relationship('Order', uselist=True, backref="payment_method")

    def __init__(self, name):
        self.name = name
        
