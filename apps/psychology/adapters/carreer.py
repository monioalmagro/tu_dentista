# Standard Libraries
from typing import List

# Third-party Libraries
from django.db.models import F, QuerySet

# Own Libraries
from apps.psychology.models import Carreer
from utils.adapter import ModelAdapter


class CarreerAdapter(ModelAdapter):
    model_class = Carreer

    def annotate_user_carreer_values(
        self,
        queryset: QuerySet[Carreer],
    ) -> QuerySet[Carreer]:
        return queryset.annotate(
            service_method=F("user_carreer_set__service_method"),
            service_modality=F("user_carreer_set__service_modality"),
            experience_summary=F("user_carreer_set__experience_summary"),
        )

    def get_queryset(self, **kwargs) -> QuerySet[Carreer]:
        queryset = super().get_queryset(**kwargs)
        queryset = queryset.prefetch_related("user_carreer_set")
        if self.user_id:
            return self.annotate_user_carreer_values(queryset=queryset)
        return queryset

    def get_objects(
        self,
        limit: int | None = None,
        offset: int | None = None,
        order_by: List[str] | None = None,
        **kwargs
    ) -> List[Carreer]:
        kwargs["is_active"] = True
        if self.user_id:
            kwargs["user_carreer_set__user_id"] = self.user_id
        return super().get_objects(limit, offset, order_by, **kwargs)


class EditableCarreerAdapter(CarreerAdapter):
    def get_objects(
        self,
        limit: int | None = None,
        offset: int | None = None,
        order_by: List[str] | None = None,
        **kwargs
    ) -> List[Carreer]:
        kwargs["is_active"] = True
        return super().get_objects(limit, offset, order_by, **kwargs)
