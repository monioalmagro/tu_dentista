# Standard Libraries
import logging
from typing import List

# Third-party Libraries
from django.db.models import QuerySet

# Own Libraries
from apps.psychology.models import Specialization
from utils.adapter import ModelAdapter

logger = logging.getLogger(__name__)


class SpecializationAdapterBase(ModelAdapter):
    model_class = Specialization

    def get_queryset(self, **kwargs) -> QuerySet[Specialization]:
        return (
            self.get_model_class()
            .objects.prefetch_related("user_specialization_set")
            .filter(**kwargs)
        )


class SpecializationAdapter(SpecializationAdapterBase):
    def get_objects(
        self,
        limit: int | None = None,
        offset: int | None = None,
        order_by: List[str] | None = None,
        **kwargs,
    ) -> List[Specialization]:
        kwargs["is_active"] = True
        if self.user_id:
            kwargs["user_specialization_set__user_id"] = self.user_id
        return super().get_objects(limit, offset, order_by, **kwargs)


class EditableSpecializationAdapter(SpecializationAdapterBase):
    def get_objects(
        self,
        limit: int | None = None,
        offset: int | None = None,
        order_by: List[str] | None = None,
        **kwargs,
    ) -> List[Specialization]:
        kwargs["is_active"] = True
        return super().get_objects(limit, offset, order_by, **kwargs)
