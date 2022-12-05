from ..models import DeliveryToolType
from .. import db
from ..utils import create_slug

delivery_tool_types = [
    {
        "name": "Moyen de déplacement rapide",
    },
    {
        "name": "Sac de coursier",
    },
    {
        "name": "Imperméable",
    },
    {
        "name": "Autres",
    },
]

class DeliveryToolTypeMigration:
    @classmethod
    def migrate(cls):
        for item in delivery_tool_types:
            delivery_tool_type = DeliveryToolType(
                item.get("name"),
                )
            db.session.add(delivery_tool_type)
            db.session.commit()
