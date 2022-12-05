from flask_login import UserMixin
from .. import db

class NotificationType(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    name = db.Column(db.String(1000))
    icon = db.Column(db.String(1000))
    background_color = db.Column(db.String(1000))

    notifications = db.relationship('Notification', uselist=True, backref="notification_type")

    def __init__(self, name, icon, background_color):
        self.name = name
        self.icon = icon
        self.background_color = background_color
        
