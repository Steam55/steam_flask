from flask_login import UserMixin
from .. import db

class Promotion(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    expire_at = db.Column(db.String(100))
    status = db.Column(db.Boolean, default=False)
    slug = db.Column(db.String(42))     # example: promotion-12562541256395874581256984571245
    discount_percentage = db.Column(db.Integer)     # inférieur ou égale à 100
    seller_id = db.Column(db.Integer, db.ForeignKey('seller.id'), nullable=False)

    products = db.relationship('Product', uselist=True, backref="promotion")

    def __init__(self, expire_at, status, slug, discount_percentage, seller_id):
        self.expire_at = expire_at
        self.status = status
        self.slug = slug
        self.discount_percentage = discount_percentage
        self.seller_id = seller_id

        
