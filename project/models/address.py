from flask_login import UserMixin
from .. import db

class Address(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(1000))
    description = db.Column(db.String(1000))
    lat = db.Column(db.Float)
    lng = db.Column(db.Float)
    is_primary = db.Column(db.Boolean, default=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)


    def __init__(self, name, description, lat, lng, is_primary, user_id):
        self.name = name
        self.description = description
        self.lat = lat
        self.lng = lng
        self.is_primary = is_primary
        self.user_id = user_id

        
