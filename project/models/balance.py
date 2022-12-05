from flask_login import UserMixin
from .. import db

class Balance(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Integer)
    updated_at = db.Column(db.String(1000))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)


    def __init__(self, amount, updated_at, user_id):
        self.amount = amount
        self.updated_at = updated_at
        self.user_id = user_id
        
