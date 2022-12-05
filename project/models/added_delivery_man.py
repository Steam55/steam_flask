from flask_login import UserMixin
from .. import db

class AddedDeliveryMan(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'), nullable=False)
    delivery_man_id = db.Column(db.Integer, db.ForeignKey('delivery_man.id'), nullable=False)


    def __init__(self, order_id, delivery_man_id):
        self.order_id = order_id
        self.delivery_man_id = delivery_man_id

        
