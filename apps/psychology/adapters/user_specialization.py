# Standard Libraries
import logging
from typing import List

# Third-party Libraries
from django.db import DatabaseError, IntegrityError, transaction
from django.db.models import QuerySet

# Own Libraries
from apps.core.models import AuthUser
from apps.psychology.models import Specialization, UserSpecialization
from utils.adapter import ModelAdapter
from utils.database import async_database

logger = logging.getLogger(__name__)


class UserSpecializationAdapter(ModelAdapter):
    model_class = UserSpecialization

    def get_queryset(self, **kwargs) -> QuerySet[UserSpecialization]:
        return (
            self.get_model_class()
            .objects.prefetch_related("user_specialization_set")
            .filter(**kwargs)
        )

    def get_objects(
        self,
        limit: int | None = None,
        offset: int | None = None,
        order_by: List[str] | None = None,
        **kwargs,
    ) -> List[UserSpecialization]:
        kwargs["is_active"] = True
        kwargs["user_specialization_set__user_id"] = self.user_id
        return super().get_objects(limit, offset, order_by, **kwargs)


class EditableUserSpecializationAdapter(UserSpecializationAdapter):
    def get_objects(
        self,
        limit: int | None = None,
        offset: int | None = None,
        order_by: List[str] | None = None,
        **kwargs,
    ) -> List[UserSpecialization]:
        kwargs["is_active"] = True
        return super().get_objects(limit, offset, order_by, **kwargs)

    @async_database()
    def bulk_create(self, user: AuthUser, specialization_list: list[Specialization]):
        logger.info(f"*** START {self.__class__.__name__}.bulk_create ***")
        try:
            model = self.get_model_class()
            objs = [
                model(user=user, specialization=specialization)
                for specialization in specialization_list
            ]
            if objs:
                with transaction.atomic():
                    model.objects.bulk_create(objs)
        except (DatabaseError, IntegrityError) as exp:
            logger.warning(f"*** INTEGRITY ERROR: {repr(exp)}***", exc_info=True)
            raise IntegrityError(str(exp)) from exp
