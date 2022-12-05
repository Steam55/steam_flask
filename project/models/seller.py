from flask_login import UserMixin
from .. import db


class Seller(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    designation = db.Column(db.String(1000))
    email = db.Column(db.String(1000))
    celphone = db.Column(db.String(100))
    description = db.Column(db.String(1000))
    profile_picture = db.Column(db.String(1000))
    cover_picture = db.Column(db.String(1000))
    address_lng = db.Column(db.Float)
    address_lat = db.Column(db.Float)
    status = db.Column(db.Integer)  # 1: en attente, 2: validé, 3: rejeté
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
        
    promotions = db.relationship('Promotion', uselist=True, backref="seller")
    products = db.relationship('Product', uselist=True, backref="seller")
    orders = db.relationship('Order', uselist=True, backref="seller")
    

    def __init__(self, designation, email, celphone, description, profile_picture, cover_picture, address_lng, address_lat, status, user_id):
        self.designation = designation
        self.email = email
        self.celphone = celphone
        self.description = description
        self.profile_picture = profile_picture
        self.cover_picture = cover_picture
        self.address_lng = address_lng
        self.address_lat = address_lat
        self.status = status
        self.user_id = user_id
