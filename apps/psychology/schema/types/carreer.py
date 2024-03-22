# Third-party Libraries
import strawberry

# Own Libraries
from apps.psychology.models import Carreer
from apps.psychology.schema.enums.user_carreer import (
    CarreerServiceMethodEnum,
    CarreerServiceModalityEnum,
)
from apps.psychology.schema.interfaces.basic_model_type import BaseModelType
from utils.enums import get_enum_instance_by_value


@strawberry.type()
class CarreerType(BaseModelType):
    service_method_enum: CarreerServiceMethodEnum | None = None
    service_modality_enum: CarreerServiceModalityEnum | None = None
    experience_summary: str | None = None
    truncate_experience_summary: str | None = None

    @classmethod
    def from_db_model(cls, instance: Carreer) -> "CarreerType":
        carreer = super().from_db_model(instance)
        carreer.service_method_enum = get_enum_instance_by_value(
            enum_class=CarreerServiceMethodEnum,
            value=instance.service_method,
        )
        carreer.service_modality_enum = get_enum_instance_by_value(
            enum_class=CarreerServiceModalityEnum,
            value=instance.service_modality,
        )
        carreer.experience_summary = instance.experience_summary
        carreer.truncate_experience_summary = cls.get_truncate_experience_summary(
            experience_summary=instance.experience_summary
        )
        return carreer

    @staticmethod
    def get_truncate_experience_summary(
        experience_summary: str | None = None,
    ) -> str:
        if experience_summary:
            return f"{experience_summary[:150]}, Ver más..."
        return ""


@strawberry.type()
class CarreerSelect2Type:
    id: strawberry.ID
    text: str

    @classmethod
    def from_db_model(cls, instance: Carreer) -> "CarreerSelect2Type":
        return cls(
            id=instance.pk,
            text=instance.name,
        )
