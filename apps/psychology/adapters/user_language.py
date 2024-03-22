# Standard Libraries
import logging
from typing import List

# Third-party Libraries
from django.db import DatabaseError, IntegrityError, transaction
from django.db.models import QuerySet

# Own Libraries
from apps.core.models import AuthUser
from apps.psychology.models import Language, UserLanguage
from utils.adapter import ModelAdapter
from utils.database import async_database

logger = logging.getLogger(__name__)


class UserLanguageAdapter(ModelAdapter):
    model_class = UserLanguage

    def get_queryset(self, **kwargs) -> QuerySet[UserLanguage]:
        queryset = (
            self.get_model_class()
            .objects.select_related(
                "user",
                "language",
            )
            .filter(**kwargs)
        )
        return queryset

    def get_objects(
        self,
        limit: int | None = None,
        offset: int | None = None,
        order_by: List[str] | None = None,
        **kwargs,
    ) -> List[UserLanguage]:
        kwargs["is_active"] = True
        return super().get_objects(limit, offset, order_by, **kwargs)

    @async_database()
    def add_languages_to_user(
        self, user: AuthUser, language_list: list[Language] | None = None
    ):
        objs = []
        language_list = language_list or []
        for language in language_list:
            objs.append(self.get_model_class()(user=user, language=language))
        if objs:
            try:
                with transaction.atomic():
                    self.get_model_class().objects.bulk_create(objs=objs)
            except (DatabaseError, IntegrityError) as exp:
                logging.warning(
                    "*** UserLanguageAdapter.add_languages_to_user, "
                    f"INTEGRITY ERROR, {str(exp)} - {repr(exp)} ***",
                    exc_info=True,
                )
                raise IntegrityError(str(exp)) from exp
