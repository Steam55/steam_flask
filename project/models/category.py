from flask_login import UserMixin
from .. import db

class Category(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    name = db.Column(db.String(1000))
    icon = db.Column(db.String(1000))
    slug = db.Column(db.String(41))     # example: category-12562541256395874581256984571245

    product_and_category = db.relationship('ProductAndCategory', uselist=True)
    

    def __init__(self, name, icon, slug):
        self.name = name
        self.icon = icon
        self.slug = slug
        
