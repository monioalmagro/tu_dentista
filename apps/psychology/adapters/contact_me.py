# Standard Libraries
import logging

# Third-party Libraries
from django.db import DatabaseError, IntegrityError, transaction

# Own Libraries
from apps.psychology.models import ContactMe
from apps.psychology.schema.inputs.contact_me import ContactMePydanticModel
from utils.adapter import ModelAdapter
from utils.database import async_database

logger = logging.getLogger(__name__)


class ContactMeAdapter(ModelAdapter):
    model_class = ContactMe

    @async_database()
    def create_new_contact(self, _input: ContactMePydanticModel):
        model_class = self.get_model_class()
        try:
            with transaction.atomic():
                obj = model_class.objects.create(
                    user_id=_input.user_id,
                    full_name=_input.full_name,
                    email=_input.email,
                    phone=_input.phone,
                    message=_input.message,
                )
            return obj
        except (DatabaseError, IntegrityError) as exp:
            logger.warning(
                "*** ContactMeAdapter.create_new_contact, INTEGRITY "
                f"ERROR, {str(exp)} - {repr(exp)} ***",
                exc_info=True,
            )
            raise IntegrityError(str(exp)) from exp
