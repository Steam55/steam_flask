from ..models import Address
from .. import db

data_address = [
    {
        "name": "address1",
        "description": "ma descript",
        "lat": 37.422,
        "lng": -122.084,
        "user_id": 2
    }
]

class AddressMigration:
    @classmethod
    def migrate(cls):
        for item in data_address:
            address = Address(
                item.get("name"), 
                item.get("description"), 
                item.get("lat"),
                item.get("lng"),
                True,
                item.get("user_id"),
                )
            db.session.add(address)
            db.session.commit()
