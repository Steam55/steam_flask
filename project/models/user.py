from flask_login import UserMixin
from .. import db

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    firstname = db.Column(db.String(1000))
    lastname = db.Column(db.String(1000))
    celphone = db.Column(db.String(100))
    password = db.Column(db.String(100))
    is_verified = db.Column(db.Boolean, default=False)
    is_admin = db.Column(db.Boolean, default=False)
    
    balance = db.relationship('Balance', uselist=False, backref="user")
    orders = db.relationship('Order', uselist=True, backref="user")
    notifications = db.relationship('Notification', uselist=True, backref="user")
    seller = db.relationship('Seller', uselist=False, backref="user")
    delivery_man = db.relationship('DeliveryMan', uselist=False, backref="user")
    cards = db.relationship('Card', uselist=True, backref="user")
    addresses = db.relationship('Address', uselist=True, backref="user")
    

    def __init__(self, firstname, lastname, celphone, password, is_verified, is_admin):
        self.firstname = firstname
        self.lastname = lastname
        self.celphone = celphone
        self.password = password
        self.is_verified = is_verified
        self.is_admin = is_admin
        
