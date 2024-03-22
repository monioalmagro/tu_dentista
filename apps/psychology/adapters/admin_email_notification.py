# Standard Libraries
import logging

# Third-party Libraries
from django.db import DatabaseError, IntegrityError, transaction

# Own Libraries
from apps.psychology import psychology_constants
from apps.psychology.models import AdminEmailNotification
from config.enviroment_vars import settings
from utils.adapter import ModelAdapter
from utils.database import async_database

logger = logging.getLogger(__name__)


class AdminEmailNotificationAdapter(ModelAdapter):
    model_class = AdminEmailNotification

    @async_database()
    def save_register(self, object_id: int, was_reported: bool):
        model = self.get_model_class()
        try:
            with transaction.atomic():
                model.objects.create(
                    object_id=object_id,
                    content_type=psychology_constants.CONTACT_ME,
                    admin_email=settings.DECIRES_EMAIL,
                    was_reported=was_reported,
                )
        except (DatabaseError, IntegrityError) as exp:
            logger.warning(
                "*** AdminEmailNotificationAdapter.save_register, INTEGRITY "
                f"ERROR, {str(exp)} - {repr(exp)} ***",
                exc_info=True,
            )
            raise IntegrityError(str(exp)) from exp
