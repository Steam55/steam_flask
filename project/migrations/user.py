from ..models import User
from .. import db
from werkzeug.security import generate_password_hash


data_user = None

def initialize():
    global data_user
    data_user = [
        {
            "firstname": "Admin",
            "lastname": "admin",
            "celphone": "62109693",
            "password": "000000",
            "is_verified": True,
            "is_admin": True,
        },
        {
            "firstname": "Anjo1",
            "lastname": "nini",
            "celphone": "22332233",
            "password": "000000",
            "is_verified": False,
            "is_admin": False,
        }
    ]

class UserMigration:
    @classmethod
    def migrate(cls):
        initialize()
        for item in data_user:
            password = item.get("password")
            user = User(
                item.get("firstname"), 
                item.get("lastname"), 
                item.get("celphone"), 
                generate_password_hash(password, method='sha256'),
                item.get("is_verified"),
                item.get("is_admin"),
            )
            db.session.add(user)
            db.session.commit()
