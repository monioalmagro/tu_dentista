# Third-party Libraries
import strawberry

# Own Libraries
from apps.psychology.models import ContactMe


@strawberry.type()
class ContactMeType:
    original_id: strawberry.ID
    was_reported: bool

    @classmethod
    def from_db_model(cls, instance: ContactMe) -> "ContactMeType":
        return cls(
            original_id=instance.pk,
            was_reported=instance.was_reported,
        )
