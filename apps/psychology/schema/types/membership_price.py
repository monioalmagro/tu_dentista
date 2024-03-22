# Third-party Libraries
import strawberry
from strawberry.scalars import JSON

# Own Libraries
from apps.psychology.models import MembershipPrice


@strawberry.type()
class MembershipPriceType:
    original_id: strawberry.ID
    membership: str | None = None
    price: float | None = None
    membership_options: JSON | None = None

    @classmethod
    def from_db_model(cls, instance: MembershipPrice) -> "MembershipPriceType":
        return cls(
            original_id=instance.pk,
            membership=getattr(instance.membership, "alias", None) or "",
            price=instance.price,
            membership_options=instance.membership_options,
        )
