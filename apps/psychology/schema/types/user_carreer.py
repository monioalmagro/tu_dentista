# Third-party Libraries
import strawberry

# Own Libraries
from apps.psychology.models import UserCarreer
from apps.psychology.schema.enums.user_carreer import (
    CarreerServiceMethodEnum,
    CarreerServiceModalityEnum,
)
from apps.psychology.schema.types.carreer import CarreerType
from utils.enums import get_enum_instance_by_value


@strawberry.type()
class UserCarreerType:
    original_id: strawberry.ID
    carreer: CarreerType
    service_method_enum: CarreerServiceMethodEnum | None = None
    service_modality_enum: CarreerServiceModalityEnum | None = None
    experience_summary: str | None = None
    truncate_experience_summary: str | None = None

    @classmethod
    def from_db_model(cls, instance: UserCarreer):
        return cls(
            original_id=instance.id,
            carreer=CarreerType.from_db_model(instance=instance.carreer),
            service_method_enum=get_enum_instance_by_value(
                enum_class=CarreerServiceMethodEnum,
                value=instance.service_method,
            ),
            service_modality_enum=get_enum_instance_by_value(
                enum_class=CarreerServiceModalityEnum,
                value=instance.service_modality,
            ),
            experience_summary=instance.experience_summary,
            truncate_experience_summary=cls.get_truncate_experience_summary(
                instance.experience_summary
            ),
        )

    @staticmethod
    def get_truncate_experience_summary(
        experience_summary: str | None = None,
    ) -> str:
        if experience_summary:
            return f"{experience_summary[:150]}, Ver más..."
        return ""
