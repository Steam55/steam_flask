from flask_login import UserMixin
from .. import db

class DeliveryZone(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(1000))
    description = db.Column(db.String(1000))
    radius = db.Column(db.Float)
    lat = db.Column(db.Float)
    lng = db.Column(db.Float)
    delivery_man_id = db.Column(db.Integer, db.ForeignKey('delivery_man.id'), nullable=False)

    
    def __init__(self, name, description, radius, lat, lng, delivery_man_id):
        self.name = name
        self.description = description
        self.radius = radius
        self.lat = lat
        self.lng = lng
        self.delivery_man_id = delivery_man_id


        
