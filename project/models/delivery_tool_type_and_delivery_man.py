from flask_login import UserMixin
from .. import db

class DeliveryToolAndDeliveryMan(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    delivery_tool_type_id = db.Column(db.Integer, db.ForeignKey('delivery_tool_type.id'), nullable=False)
    delivery_man_id = db.Column(db.Integer, db.ForeignKey('delivery_man.id'), nullable=False)

    def __init__(self, delivery_tool_type_id, delivery_man_id):
        self.delivery_tool_type_id = delivery_tool_type_id
        self.delivery_man_id = delivery_man_id

        
