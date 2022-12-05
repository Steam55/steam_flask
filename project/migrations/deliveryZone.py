from ..models import DeliveryZone
from .. import db

data_delivery_zone = [
    {
        "name": "Zone",
        "description": "ma descript",
        "radius": 50,
        "lat": 37.422,
        "lng": -122.084,
        "delivery_man_id": 1
    }
]

class DeliveryZoneMigration:
    @classmethod
    def migrate(cls):
        for item in data_delivery_zone:
            delivery_zone = DeliveryZone(
                item.get("name"), 
                item.get("description"), 
                item.get("radius"),
                item.get("lat"),
                item.get("lng"),
                item.get("delivery_man_id"),
                )
            db.session.add(delivery_zone)
            db.session.commit()
