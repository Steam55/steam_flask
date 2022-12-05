from flask_login import UserMixin
from .. import db

class Order(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    quantity = db.Column(db.Integer)
    product_final_price = db.Column(db.Float)
    status = db.Column(db.Integer)
    slug = db.Column(db.String(38))     # example: order-12562541256395874581256984571245
    user_address_lng = db.Column(db.Float)
    user_address_lat = db.Column(db.Float)
    seller_id = db.Column(db.Integer, db.ForeignKey('seller.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    payment_method_id = db.Column(db.Integer, db.ForeignKey('payment_method.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)


    added_delivery_man = db.relationship('AddedDeliveryMan', uselist=False, backref="order")

    def __init__(self, quantity, product_final_price, status, slug, user_address_lng, user_address_lat, seller_id, product_id, payment_method_id, user_id):
        self.quantity = quantity
        self.product_final_price = product_final_price
        self.status = status
        self.slug = slug
        self.user_address_lng = user_address_lng
        self.user_address_lat = user_address_lat
        self.seller_id = seller_id
        self.product_id = product_id
        self.payment_method_id = payment_method_id
        self.user_id = user_id

        
