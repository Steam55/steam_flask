from flask_login import UserMixin
from .. import db


class Product(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(1000))
    image = db.Column(db.String(1000))
    primary_price = db.Column(db.Float) # product-12562541256395874581256984571245
    slug = db.Column(db.String(40))
    description = db.Column(db.String(1000))
    is_available = db.Column(db.Boolean, default=False)
    hot = db.Column(db.Boolean, default=False)
    note = db.Column(db.Float)
    promotion_id = db.Column(db.Integer, db.ForeignKey('promotion.id'), nullable=False)
    seller_id = db.Column(db.Integer, db.ForeignKey('seller.id'), nullable=False)

    orders = db.relationship('Order', uselist=True, backref="product")
    cart_products = db.relationship('CartProduct', uselist=True, backref="product")


    def __init__(self, name, image, primary_price, slug, description, is_available, hot, note, promotion_id, seller_id):
        self.name = name
        self.image = image
        self.primary_price = primary_price
        self.slug = slug
        self.description = description
        self.is_available = is_available
        self.hot = hot
        self.note = note
        self.promotion_id = promotion_id
        self.seller_id = seller_id
