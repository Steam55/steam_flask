from flask_login import UserMixin
from .. import db

class Notification(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    message = db.Column(db.String(1000))
    seen = db.Column(db.Boolean)
    order_identifier = db.Column(db.String(1000))   # optionnel, n'est fourni que lorsque la notification est en rapport à une commande
    type_id = db.Column(db.Integer, db.ForeignKey('notification_type.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)



    def __init__(self, message, seen, order_identifier, type_id, user_id):
        self.message = message
        self.seen = seen
        self.order_identifier = order_identifier
        self.type_id = type_id
        self.user_id = user_id
        
