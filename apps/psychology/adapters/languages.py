# Standard Libraries
from typing import List

# Own Libraries
from apps.psychology.models import Language
from utils.adapter import ModelAdapter


class LanguageAdapter(ModelAdapter):
    model_class = Language

    def get_object(self, **kwargs) -> Language | None:
        kwargs["is_active"] = True
        kwargs["user_language_set__user_id"] = self.user_id
        return super().get_object(**kwargs)

    def get_objects(
        self,
        limit: int | None = None,
        offset: int | None = None,
        order_by: List[str] | None = None,
        **kwargs,
    ) -> List[Language]:
        kwargs["is_active"] = True
        if self.user_id:
            kwargs["user_language_set__user_id"] = self.user_id
        return super().get_objects(limit, offset, order_by, **kwargs)


class EditableLanguageAdapter(ModelAdapter):
    model_class = Language

    def get_object(self, **kwargs) -> Language | None:
        kwargs["is_active"] = True
        return super().get_object(**kwargs)

    def get_objects(
        self,
        limit: int | None = None,
        offset: int | None = None,
        order_by: List[str] | None = None,
        **kwargs,
    ) -> List[Language]:
        kwargs["is_active"] = True
        return super().get_objects(limit, offset, order_by, **kwargs)
