# Standard Libraries
from typing import Type

# Third-party Libraries
from django.db import IntegrityError
from django.db.models import Q
from strawberry.types import Info

# Own Libraries
from apps.core.models import AuthUser
from apps.psychology.adapters.carreer import EditableCarreerAdapter
from apps.psychology.adapters.contact_me import ContactMeAdapter
from apps.psychology.adapters.languages import EditableLanguageAdapter
from apps.psychology.adapters.specialization import (
    EditableSpecializationAdapter,
)
from apps.psychology.adapters.user import UserAdapter
from apps.psychology.adapters.user_attachments import (
    EditableUserAttachmentAdapter,
)
from apps.psychology.adapters.user_carreer import UserCarreerAdapter
from apps.psychology.adapters.user_language import UserLanguageAdapter
from apps.psychology.adapters.user_specialization import (
    EditableUserSpecializationAdapter,
)
from apps.psychology.adapters.user_zone import UserZoneAdapter
from apps.psychology.adapters.zone import EditableZoneAdapter
from apps.psychology.models import ContactMe
from apps.psychology.schema.background_tasks.send_admin_email_notifications import (
    send_message_to_admin_and_professional,
)
from apps.psychology.schema.inputs.contact_me import ContactMePydanticModel
from apps.psychology.schema.inputs.user import MutationUserPydanticModel
from apps.psychology.schema.inputs.user_carreer import UserCarreerPydanticModel
from apps.psychology.schema.interfaces.process import (
    BaseMutationProcess,
    BaseValidator,
)
from utils.send_email import prepare_data_new_professional


class BaseUserProcess(BaseMutationProcess):
    def __init__(self, validator_instance: Type[BaseValidator]):
        super().__init__(validator_instance)

    def get_user_adapter(self):
        return UserAdapter()


##
class ContactProfessionalValidator(BaseValidator):
    def __init__(self, _input: ContactMePydanticModel):
        super().__init__(_input)

    async def validation_controller(self, user_adapter: UserAdapter):
        await self._validate_user_by_id(user_adapter=user_adapter)

    async def _validate_user_by_id(self, user_adapter: UserAdapter):
        _input = self.input
        if not (await user_adapter.get_object(**{"id": _input.user_id})):
            raise AssertionError(f"User not found with ID: {_input.user_id}")


class ContactProfessionalProcess(BaseUserProcess):
    def __init__(
        self,
        validator_instance: ContactProfessionalValidator,
        _input: ContactMePydanticModel,
    ):
        super().__init__(validator_instance)
        self.validator = validator_instance
        self.user_adapter = self.get_user_adapter()
        self.contact_me_adapter = self.get_contact_me_adapter()
        self.input = _input

    def get_contact_me_adapter(self):
        return ContactMeAdapter()

    @staticmethod
    async def send_background_tasks(
        info: Info,
        callable_function: callable,
        adapter: ContactMeAdapter,
        instance: ContactMe,
    ):
        background_tasks = info.context["background_tasks"]
        background_tasks.add_task(callable_function, adapter, instance)

    async def action(self, info: Info) -> ContactMe | None:
        adapter = self.contact_me_adapter
        _validator = self.validator
        await _validator.validation_controller(user_adapter=self.user_adapter)

        if contact_me_instance := await adapter.create_new_contact(_input=self.input):
            await self.send_background_tasks(
                info=info,
                callable_function=send_message_to_admin_and_professional,
                adapter=adapter,
                instance=contact_me_instance,
            )

            return contact_me_instance


##
class ProfessionalValidator(BaseValidator):
    def __init__(self, _input: MutationUserPydanticModel):
        super().__init__(_input)

    async def _validate_user_unique(self, user_adapter: UserAdapter):
        user_unique_filter = (
            Q(email=self.input.email)
            | Q(nro_dni=self.input.nro_dni)
            | Q(nro_matricula=self.input.nro_matricula)
            | Q(cuit=self.input.cuit)
        )

        if facebook_profile := self.input.facebook_profile:
            user_unique_filter |= Q(**{"facebook_profile": facebook_profile})
        if instagram_profile := self.input.instagram_profile:
            user_unique_filter |= Q(**{"instagram_profile": instagram_profile})
        if linkedin_profile := self.input.linkedin_profile:
            user_unique_filter |= Q(**{"linkedin_profile": linkedin_profile})

        if await user_adapter.get_object(
            user_unique_filter=user_unique_filter,
            user_exclude={
                "facebook_profile__isnull": True,
                "instagram_profile__isnull": True,
                "linkedin_profile__isnull": True,
            },
        ):
            raise IntegrityError(
                "Invalid registration. The provided information is "
                "already in use. Please check your details and try again",
            )

    async def validation_controller(self, user_adapter: UserAdapter):
        await self._validate_user_unique(user_adapter=user_adapter)


class NewProfessionalProcess(BaseUserProcess):
    def __init__(
        self,
        validator_instance: ProfessionalValidator,
        _input: MutationUserPydanticModel,
    ):
        super().__init__(validator_instance)
        self.validator = validator_instance
        self.user_adapter = self.get_user_adapter()
        self.zone_adapter = self.get_zone_adapter()
        self.user_zone_adapter = self.get_user_zone_adapter()
        self.carreer_adapter = self.get_carreer_adapter()
        self.user_carreer_adapter = self.get_user_carreer_adapter()
        self.specialization_adapter = self.get_specialization_adapter()
        self.user_specialization_adapter = self.get_user_specialization_adapter()
        self.language_adapter = self.get_language_adapter()
        self.user_language_adapter = self.get_user_language_adapter()
        self.user_attachment_adapter = self.get_user_attachment_adapter()
        self.input = _input

    def get_user_attachment_adapter(self):
        return EditableUserAttachmentAdapter()

    def get_user_specialization_adapter(self):
        return EditableUserSpecializationAdapter()

    def get_zone_adapter(self):
        return EditableZoneAdapter()

    def get_user_zone_adapter(self):
        return UserZoneAdapter()

    def get_user_carreer_adapter(self):
        return UserCarreerAdapter()

    def get_carreer_adapter(self):
        return EditableCarreerAdapter()

    def get_specialization_adapter(self):
        return EditableSpecializationAdapter()

    def get_language_adapter(self):
        return EditableLanguageAdapter()

    def get_user_language_adapter(self):
        return UserLanguageAdapter()

    async def add_office_locations(self, professional: AuthUser):
        self.zone_adapter.user_id = professional.id

        if zone_list := await self.zone_adapter.get_objects(
            id__in=self.input.office_locations
        ):
            await self.user_zone_adapter.bulk_create(
                user_id=professional.id,
                zone_list=zone_list,
            )

    async def add_carreer(self, professional: AuthUser):
        self.carreer_adapter.user_id = professional.id

        if carreer := await self.carreer_adapter.get_object(id=self.input.carreer):
            data = UserCarreerPydanticModel(
                user_id=professional.id,
                carreer_id=carreer.id,
                service_method=self.input.service_method_enum,
                service_modality=self.input.service_modality_enum,
                experience_summary=self.input.experience_summary,
            )

            await self.user_carreer_adapter.add_carrers_to_user(
                data=data,
            )

    async def add_specialization(self, professional: AuthUser):
        self.specialization_adapter.user_id = professional.id
        self.user_specialization_adapter.user_id = professional.id
        specializations = await self.specialization_adapter.get_objects(id__in=[2])
        if self.input.specializations and (
            specializations := await self.specialization_adapter.get_objects(
                id__in=self.input.specializations
            )
        ):
            await self.user_specialization_adapter.bulk_create(
                user=professional,
                specialization_list=specializations,
            )

    async def add_languages(self, professional: AuthUser):
        if language := await self.language_adapter.get_objects(
            id__in=self.input.languages
        ):
            await self.user_language_adapter.add_languages_to_user(
                user=professional, language_list=language
            )

    async def user_set_password(self, adapter: UserAdapter, professional: AuthUser):
        await adapter.set_password(
            obj=professional,
            password=self.input.password,
        )

    async def add_attachments(self, professional: AuthUser):
        await self.user_attachment_adapter.associate_attachment_to_user(
            user=professional,
            attachment_id_list=self.input.attachment_ids,
        )

    async def action(self, info: Info | None = None) -> AuthUser | None:
        adapter = self.user_adapter
        await self.validator.validation_controller(user_adapter=self.user_adapter)
        if new_professional := await adapter.create_new_professional(self.input):
            await self.user_set_password(
                adapter=adapter,
                professional=new_professional,
            )
            await self.add_office_locations(
                professional=new_professional,
            )
            await self.add_languages(professional=new_professional)
            await self.add_carreer(professional=new_professional)
            await self.add_specialization(professional=new_professional)
            await self.add_attachments(professional=new_professional)
            await prepare_data_new_professional(new_professional)
            return new_professional


##
