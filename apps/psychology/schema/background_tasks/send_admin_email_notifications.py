# Standard Libraries
import logging

# Third-party Libraries
from django.db import IntegrityError
from django.utils import timezone

# Own Libraries
from apps.psychology.adapters.admin_email_notification import (
    AdminEmailNotificationAdapter,
)
from apps.psychology.adapters.contact_me import ContactMeAdapter
from apps.psychology.models import ContactMe
from utils.send_email import prepare_data_contact_me

logger = logging.getLogger(__name__)


async def send_message_to_admin_and_professional(
    adapter: ContactMeAdapter,
    contact_me_instance: ContactMe,
):
    # send email to professional and email to admin
    try:
        contact_me_instance.was_reported = True
        contact_me_instance.updated_at = timezone.now()

        _contact_me_instance: ContactMe = await adapter.save_obj(
            obj=contact_me_instance,
            update_fields=[
                "was_reported",
                "updated_at",
            ],
        )

        # LOGIC: SEND MSG TO WHATSAPP AND EMAIL TO ADMIN AND PROFESSIONAL
        await prepare_data_contact_me(contact_me_instance)

        history_adapter = AdminEmailNotificationAdapter()
        await history_adapter.save_register(
            object_id=_contact_me_instance.pk,
            was_reported=_contact_me_instance.was_reported,
        )
    except IntegrityError as exp:
        logger.warning(
            f"***BACKGROUND TASKS INTEGRITY ERROR {str(exp)} - {repr(exp)}***",
            exc_info=True,
        )
