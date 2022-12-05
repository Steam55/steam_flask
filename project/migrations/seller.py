from ..models import Seller
from .. import db
from werkzeug.security import generate_password_hash


data_seller = None

def initialize():
    global data_seller
    data_seller = [
        {
            "designation": "Restau U",
            "email": "papananvenza@gmail.com",
            "celphone": "+229 62109693",
            "description": "Description de mon restaurant",
            "profile_picture": "",
            "cover_picture": "",
            "address_lng": -122.084,
            "address_lat": 37.422,
            "user_id": 1
        },
    ]
     
     
class SellerMigration:
    @classmethod
    def migrate(cls):
        initialize()
        for item in data_seller:
            seller = Seller(
                item.get("designation"), 
                item.get("email"), 
                item.get("celphone"),
                item.get("description"),
                item.get("profile_picture"), 
                item.get("cover_picture"), 
                item.get("address_lng"), 
                item.get("address_lat"), 
                2,
                item.get("user_id"),
            )
            db.session.add(seller)
            db.session.commit()
