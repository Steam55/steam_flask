from flask_login import UserMixin
from .. import db

class Restaurant(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    name = db.Column(db.String(1000))
    celphone = db.Column(db.String(100))
    email = db.Column(db.String(100))
    description = db.Column(db.String(1000))
    profile_picture = db.Column(db.String(1000))
    cover_picture = db.Column(db.String(1000))
    address_lng = db.Column(db.Float)
    address_lat = db.Column(db.Float)
    # restaurant_address_id = db.Column(db.Integer, db.ForeignKey('restaurant_address.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __init__(self, name, celphone, email, description, profile_picture, cover_picture, address_lng, address_lat, user_id):
        self.name = name
        self.celphone = celphone
        self.email = email
        self.description = description
        self.profile_picture = profile_picture
        self.cover_picture = cover_picture
        self.address_lng = address_lng
        self.address_lat = address_lat
        self.user_id = user_id
        
