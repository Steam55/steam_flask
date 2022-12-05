from flask_login import UserMixin
from .. import db

class Delivery(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Integer)
    made_at = db.Column(db.String(100))
    status = db.Column(db.Integer) # 1: acceptée, 2: entamée, 3: effectuée
    slug = db.Column(db.String(41))     # example: delivery-12562541256395874581256984571245
    order_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    delivery_man_id = db.Column(db.Integer, db.ForeignKey('delivery_man.id'), nullable=False)


    def __init__(self, amount, made_at, status, slug, order_id, delivery_man_id):
        self.amount = amount
        self.made_at = made_at
        self.status = status
        self.slug = slug
        self.order_id = order_id
        self.delivery_man_id = delivery_man_id

        
