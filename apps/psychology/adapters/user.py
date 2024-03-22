# Standard Libraries
import logging
from typing import List

# Third-party Libraries
from django.db import DatabaseError, IntegrityError, transaction
from django.db.models import F, QuerySet

# Own Libraries
from apps.core.models import AuthUser
from apps.psychology.schema.inputs.user import MutationUserPydanticModel
from utils.adapter import ModelAdapter
from utils.database import async_database

logger = logging.getLogger(__name__)


class UserAdapter(ModelAdapter):
    model_class = AuthUser

    def get_queryset(self, **kwargs) -> QuerySet[AuthUser]:
        return (
            self.get_model_class()
            .objects.filter(**kwargs)
            .annotate(
                type=F("user_payment_set__type"),
            )
        )

    @async_database()
    def get_object(self, **kwargs) -> AuthUser | None:
        logger.info(f"*** KWARGS: {kwargs} ***")
        if "is_active" not in kwargs:
            kwargs["is_active"] = True
        user_unique_filter = kwargs.pop("user_unique_filter", None)
        user_exclude = kwargs.pop("user_exclude", None)

        queryset = self.get_queryset(**kwargs)

        if user_unique_filter:
            queryset = queryset.filter(user_unique_filter)
        if user_exclude:
            queryset = queryset.exclude(**user_exclude)

        return queryset.first()

    @async_database()
    def get_objects(
        self,
        limit: int | None = None,
        offset: int | None = None,
        order_by: List[str] | None = None,
        **kwargs,
    ) -> list[AuthUser]:
        logger.debug(f"*** {self.__class__.__name__}.get_objects ***")
        if "is_active" not in kwargs:
            kwargs["is_active"] = True

        limit = limit or self.default_limit
        offset = offset or 0

        queryset = self.get_queryset(**kwargs)

        if order_by:
            queryset = queryset.order_by(*order_by)

        queryset = queryset[offset : offset + limit]

        return set(queryset)

    @async_database()
    def create_new_professional(self, _input: MutationUserPydanticModel):
        model = self.get_model_class()
        try:
            with transaction.atomic():
                obj = model.objects.create(
                    email=_input.email,
                    username=_input.email,
                    first_name=_input.first_name,
                    last_name=_input.last_name,
                    nro_dni=_input.nro_dni,
                    nro_matricula=_input.nro_matricula,
                    cuit=_input.cuit,
                    phone=_input.phone,
                    gender=_input.gender_enum,
                    facebook_profile=_input.facebook_profile,
                    instagram_profile=_input.instagram_profile,
                    linkedin_profile=_input.linkedin_profile,
                    personal_address=_input.personal_address,
                    membership_plan=_input.membership_plan_enum,
                    attention_schedule=_input.attention_schedule,
                )
            return obj
        except (DatabaseError, IntegrityError) as exp:
            logger.warning(
                "*** UserAdapter.create_new_professional, INTEGRITY "
                f"ERROR, {str(exp)} - {repr(exp)} ***",
                exc_info=True,
            )
            raise IntegrityError(str(exp)) from exp

    @async_database()
    def set_password(self, obj: AuthUser, password: str):
        obj.set_password(password)
        obj.save(update_fields=["password"])
