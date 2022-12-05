from flask_login import UserMixin
from .. import db

class DeliveryMan(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    can_make_delivery = db.Column(db.Boolean)
    accept_responsibilities = db.Column(db.Boolean)
    about_you = db.Column(db.String(1000))
    can_make_video_conference = db.Column(db.Boolean)
    status = db.Column(db.Integer)  # 1: en attente, 2: validé, 3: rejeté
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    deliveries = db.relationship('Delivery', uselist=True, backref="delivery_man")
    delivery_zones = db.relationship('DeliveryZone', uselist=True, backref="delivery_man")
    added_delivery_mans = db.relationship('AddedDeliveryMan', uselist=True, backref="delivery_man")

    def __init__(self, can_make_delivery, accept_responsibilities, about_you, can_make_video_conference, status, user_id):
        self.can_make_delivery = can_make_delivery
        self.accept_responsibilities = accept_responsibilities
        self.about_you = about_you
        self.can_make_video_conference = can_make_video_conference
        self.status = status
        self.user_id = user_id
