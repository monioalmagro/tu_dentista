# Standard Libraries
import logging
from typing import List

# Third-party Libraries
from django.db import DatabaseError, IntegrityError, transaction

# Own Libraries
from apps.psychology.models import UserCarreer
from apps.psychology.schema.inputs.user_carreer import UserCarreerPydanticModel
from utils.adapter import ModelAdapter
from utils.database import async_database

logger = logging.getLogger(__name__)


class UserCarreerAdapter(ModelAdapter):
    model_class = UserCarreer

    def get_objects(
        self,
        limit: int | None = None,
        offset: int | None = None,
        order_by: List[str] | None = None,
        **kwargs,
    ) -> List[UserCarreer]:
        kwargs["is_active"] = True
        return super().get_objects(limit, offset, order_by, **kwargs)

    @async_database()
    def add_carrers_to_user(
        self,
        data: UserCarreerPydanticModel,
    ):
        try:
            _data = data.dict(exclude_none=True)
            with transaction.atomic():
                self.get_model_class().objects.create(**_data)
        except (DatabaseError, IntegrityError) as exp:
            logging.warning(
                "*** UserCarreerAdapter.add_carrers_to_user, "
                f"INTEGRITY ERROR, {str(exp)} - {repr(exp)} ***",
                exc_info=True,
            )
            raise IntegrityError(str(exp)) from exp
