from ..models import PaymentMethod
from .. import db
from ..utils import create_slug

payment_methods = [
    {
        "name": "MTN Mobile Money",
    },
    {
        "name": "Moov Money",
    },
    {
        "name": "Mon solde Steam",
    }
]

class PaymentMethodMigration:
    @classmethod
    def migrate(cls):
        for item in payment_methods:
            payment_method = PaymentMethod(
                item.get("name"),
                )
            db.session.add(payment_method)
            db.session.commit()
