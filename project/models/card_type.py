from flask_login import UserMixin
from .. import db

class CardType(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(1000))

    cards = db.relationship('Card', uselist=True, backref="card_type")

    def __init__(self, name):
        self.name = name

        
