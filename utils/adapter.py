# Standard Libraries
import logging
from typing import List, Optional, Type, TypeVar

# Third-party Libraries
from django.db import models
from django.db.models import QuerySet

# Own Libraries
from utils.database import async_database

logger = logging.getLogger(__name__)

ModelT = TypeVar("ModelT", bound=models.Model)


class ModelAdapter:
    model_class: Type[ModelT] = None
    default_limit = 1000
    _log_tag = None
    _user_id = None

    @property
    def user_id(self):
        return self._user_id

    @user_id.setter
    def user_id(self, value: int):
        self._user_id = value

    @async_database()
    def save_obj(self, obj: Type[ModelT], update_fields: list[str] | None = None):
        logger.info(f"*** Start {self.__class__.__name__}.save_obj ***")
        if update_fields := update_fields or []:
            obj.save(update_fields=update_fields)
        else:
            obj.save()
        return obj

    @async_database()
    def get_object(self, **kwargs) -> Optional[ModelT]:
        logger.info(f"*** Start {self.__class__.__name__}.get_object ***")
        instance = self.get_queryset(**kwargs)

        return instance.first() if instance.exists() else None

    def get_model_class(self) -> ModelT:
        if not self.model_class:
            raise NotImplementedError("Define model_class attr")
        return self.model_class

    def get_queryset(self, **kwargs) -> QuerySet[ModelT]:
        return self.get_model_class().objects.filter(**kwargs)

    @async_database()
    def get_objects(
        self,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
        order_by: Optional[List[str]] = None,
        **kwargs,
    ) -> List[ModelT]:
        logger.info(f"*** Start {self.__class__.__name__}.get_objects ***")
        limit = limit or self.default_limit
        offset = offset or 0

        queryset = self.get_queryset(**kwargs)

        if order_by:
            queryset = queryset.order_by(*order_by)

        queryset = queryset[offset : offset + limit]

        return list(queryset)
