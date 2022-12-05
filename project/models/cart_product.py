from flask_login import UserMixin
from .. import db


class CartProduct(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(1000))
    image = db.Column(db.String(1000))
    primary_price = db.Column(db.Float)
    quantity = db.Column(db.Integer)
    product_id = db.Column(db.Integer, db.ForeignKey(
        'product.id'), nullable=False)
    # promotion_id = db.Column(db.Integer, db.ForeignKey('promotion.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)


    def __init__(self, name, image, primary_price, quantity, product_id, user_id):
        self.name = name
        self.image = image
        self.primary_price = primary_price
        self.quantity = quantity
        self.product_id = product_id
        # self.promotion_id = promotion_id
        self.user_id = user_id
