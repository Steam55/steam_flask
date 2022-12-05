from ..models import Promotion
from .. import db
from ..utils import create_slug

data_promotions = [
    {
        "expire_at": "",
        "status": True,
        "discount_percentage": 0,
        "seller_id": 1
    }
]

class PromotionMigration:
    @classmethod
    def migrate(cls):
        for item in data_promotions:
            slug = create_slug()
            promotion = Promotion(
                item.get("expire_at"),
                item.get("status"),
                "promotion-" + slug,
                item.get("discount_percentage"), 
                item.get("seller_id")
                )
            db.session.add(promotion)
            db.session.commit()
