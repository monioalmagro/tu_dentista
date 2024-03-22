# Standard Libraries
import logging
from typing import List

# Third-party Libraries
from django.db import DatabaseError, IntegrityError, transaction

# Own Libraries
from apps.core.models import UserZone, Zone
from utils.adapter import ModelAdapter
from utils.database import async_database

logger = logging.getLogger(__name__)


class UserZoneAdapter(ModelAdapter):
    model_class = UserZone

    def get_objects(
        self,
        limit: int | None = None,
        offset: int | None = None,
        order_by: List[str] | None = None,
        **kwargs,
    ) -> List[UserZone]:
        kwargs["is_active"] = True
        kwargs["user_id"] = self.user_id
        return super().get_objects(limit, offset, order_by, **kwargs)

    @async_database()
    def bulk_create(self, user_id: int, zone_list: list[Zone]) -> list[UserZone]:
        logger.info(f"*** Start {self.__class__.__name__}.bulk_create ***")
        try:
            model = self.get_model_class()
            objs = [model(user_id=user_id, zone=zone) for zone in zone_list]
            if objs:
                with transaction.atomic():
                    model.objects.bulk_create(objs)
        except (DatabaseError, IntegrityError) as exp:
            logger.warning(
                f"***{self.__class__.__name__}.bulk_create INTEGRITY ERROR***"
            )
            logger.warning(f"***{repr(exp)} ***", exc_info=True)
            raise IntegrityError(str(exp)) from exp
