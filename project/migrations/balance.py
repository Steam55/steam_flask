from ..models import Balance
from .. import db

data_balance = [
    {
        "amount": 0,
        "updated_at": "08/09/2022 15:09",
        "user_id": 1,
    },
    {
        "amount": 0,
        "updated_at": "08/09/2022 15:09",
        "user_id": 2,
    }
]

class BalanceMigration:
    @classmethod
    def migrate(cls):
        for item in data_balance:
            balance = Balance(
                item.get("amount"), 
                item.get("updated_at"), 
                item.get("user_id"),
                )
            db.session.add(balance)
            db.session.commit()
