# Standard Libraries
from typing import Self, TypeVar

# Third-party Libraries
import strawberry
from django.db import models

_TModel = TypeVar("_TModel", bound=models.Model)


@strawberry.interface()
class BaseModelType:
    original_id: strawberry.ID
    name: str | None = None
    description: str | None = None

    @classmethod
    def from_db_model(cls, instance: _TModel) -> Self:
        return cls(
            original_id=instance.id,
            name=instance.name,
            description=instance.description,
        )
