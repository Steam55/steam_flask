from flask_login import UserMixin
from .. import db

class Card(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    uploaded_at = db.Column(db.String(1000))
    image = db.Column(db.String(1000))
    type_id = db.Column(db.Integer, db.ForeignKey('card_type.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    
    def __init__(self, uploaded_at, image, type_id, user_id):
        self.uploaded_at = uploaded_at
        self.image = image
        self.type_id = type_id
        self.user_id = user_id
        
