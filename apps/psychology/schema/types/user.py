# Third-party Libraries
import strawberry

# Own Libraries
from apps.core.models import AuthUser
from apps.psychology.adapters.carreer import CarreerAdapter
from apps.psychology.adapters.languages import LanguageAdapter
from apps.psychology.adapters.specialization import SpecializationAdapter
from apps.psychology.adapters.user_attachments import UserAttachmentAdapter
from apps.psychology.adapters.zone import ZoneAdapter
from apps.psychology.models import UserAttachment
from apps.psychology.schema.enums.auth_user import (
    AuthUserGenderEnum,
    AuthUserMembershipPlanEnum,
)
from apps.psychology.schema.types.carreer import CarreerType
from apps.psychology.schema.types.city import ZoneType
from apps.psychology.schema.types.specialization import SpecializationType
from apps.psychology.schema.types.user_language import LanguageType
from utils.enums import get_enum_instance_by_value


@strawberry.type()
class AttachmentType:
    original_id: strawberry.ID | None = None
    url: str | None = None
    description: str | None = None

    @classmethod
    def from_db_model(cls, instance: UserAttachment):
        return cls(
            original_id=instance.pk,
            url=instance.url_content,
            description=instance.description,
        )


@strawberry.interface()
class UserType:
    original_id: strawberry.ID
    first_name: str | None = None
    last_name: str | None = None
    email: str | None = None
    gender_enum: AuthUserGenderEnum | None = None
    membership_plan_enum: AuthUserMembershipPlanEnum | None = None
    attention_schedule: str | None = None
    default_profile_picture: strawberry.Private[str]

    @classmethod
    def from_db_models(cls, instance: AuthUser) -> "UserType":
        return cls(
            original_id=instance.pk,
            first_name=instance.first_name,
            last_name=instance.last_name,
            email=instance.email,
            gender_enum=instance.gender,
            membership_plan_enum=instance.membership_plan,
            attention_schedule=instance.attention_schedule,
            default_profile_picture=instance.default_profile_picture,
        )

    @strawberry.field()
    async def avatar(self) -> AttachmentType | None:
        adapter = UserAttachmentAdapter()
        adapter.user_id = self.original_id
        if instance := await adapter.get_object(
            **{"source_content_type": UserAttachment.USER_IMAGE}
        ):
            return AttachmentType.from_db_model(instance=instance)
        return AttachmentType(
            original_id=None,
            url=self.default_profile_picture,
            description="PROFILE AVATAR",
        )


@strawberry.type()
class ProfessionalType(UserType):
    phone: str | None = None
    gender_enum: AuthUserGenderEnum | None = None
    facebook_profile: str | None = None
    instagram_profile: str | None = None
    linkedin_profile: str | None = None
    is_verified_profile: bool = False
    profile_url: str | None = None

    @classmethod
    def from_db_models(cls, instance: AuthUser) -> UserType:
        professional = super().from_db_models(instance)
        professional.phone = instance.phone
        professional.gender_enum = get_enum_instance_by_value(
            enum_class=AuthUserGenderEnum,
            value=instance.gender,
        )
        professional.facebook_profile = instance.facebook_profile
        professional.instagram_profile = instance.instagram_profile
        professional.linkedin_profile = instance.linkedin_profile
        professional.is_verified_profile = instance.is_verified_profile
        professional.profile_url = instance.profile_url
        return professional

    @strawberry.field()
    async def user_carreer_set(self) -> list[CarreerType]:
        adapter = CarreerAdapter()
        adapter.user_id = self.original_id
        if results := await adapter.get_objects():
            return [CarreerType.from_db_model(instance=carreer) for carreer in results]
        return []

    @strawberry.field()
    async def user_specialization_set(self) -> list[SpecializationType]:
        adapter = SpecializationAdapter()
        adapter.user_id = self.original_id
        if results := await adapter.get_objects():
            return [
                SpecializationType.from_db_model(instance=carreer)
                for carreer in results
            ]
        return []

    @strawberry.field()
    async def languages_set(self) -> list[LanguageType]:
        adapter = LanguageAdapter()
        adapter.user_id = self.original_id
        if results := await adapter.get_objects():
            return [
                LanguageType.from_db_model(instance=language) for language in results
            ]
        return []

    @strawberry.field()
    async def user_office_set(self) -> list[ZoneType]:
        adapter = ZoneAdapter()
        adapter.user_id = self.original_id
        if results := await adapter.get_objects():
            return [ZoneType.from_db_model(instance=zone) for zone in results]
        return []

    @strawberry.field()
    async def attachment_set(self) -> list[AttachmentType]:
        adapter = UserAttachmentAdapter()
        adapter.user_id = self.original_id

        if results := await adapter.get_objects(
            **{
                "source_content_type__in": [
                    UserAttachment.USER_DNI,
                    UserAttachment.USER_MATRICULA,
                ]
            },
        ):
            return [
                AttachmentType.from_db_model(instance=attachment_instance)
                for attachment_instance in results
            ]
        return []
