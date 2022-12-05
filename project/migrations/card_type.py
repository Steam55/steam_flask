from ..models import CardType
from .. import db
from ..utils import create_slug

card_types = [
    {
        "name": "identity_card",
    },
    {
        "name": "passport",
    },
]

class CardTypeMigration:
    @classmethod
    def migrate(cls):
        for item in card_types:
            card_type = CardType(
                item.get("name"),
                )
            db.session.add(card_type)
            db.session.commit()
