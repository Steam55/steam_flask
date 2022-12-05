from flask_login import UserMixin
from .. import db

class ProductAndCategory(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)

    
    def __init__(self, product_id, category_id):
        self.product_id = product_id
        self.category_id = category_id

        
