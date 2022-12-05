from ..models import NotificationType
from .. import db
from ..utils import create_slug

notification_types = [
    {
        "name": "order",
        "icon": "Icons.order",
        "background_color": "Colors.blue"
    },
    {
        "name": "welcome",
        "icon": "Icons.smile",
        "background_color": "Colors.green"
    },
]

class NotificationTypeMigration:
    @classmethod
    def migrate(cls):
        for item in notification_types:
            card_type = NotificationType(
                item.get("name"),
                item.get("icon"),
                item.get("background_color"),
                )
            db.session.add(card_type)
            db.session.commit()
