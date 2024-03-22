# Standard Libraries
from typing import List

# Own Libraries
from apps.core.models import City
from utils.adapter import ModelAdapter


class CityAdapter(ModelAdapter):
    model_class = City

    def get_objects(
        self,
        limit: int | None = None,
        offset: int | None = None,
        order_by: List[str] | None = None,
        **kwargs
    ) -> List[City]:
        kwargs["is_active"] = True
        return super().get_objects(limit, offset, order_by, **kwargs)
