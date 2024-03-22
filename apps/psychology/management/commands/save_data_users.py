import logging

from apps.core.models.auth_user import AbstractUser
from django.core import serializers
from django.core.management.base import BaseCommand
from apps.psychology.adapters.user import UserAdapter
from apps.psychology.schema.types.user import ProfessionalType

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Create a json with specific data of any model"

    async def generate_data(self):
        # [user_staff, user_premium, user_with_org, professor]
        adapter = UserAdapter()
        kwargs = {
            "id": input.original_id,
            "is_verified_profile": True,
        }
        if result := await adapter.get_object(**kwargs):
            return ProfessionalType.from_db_models(instance=result)
        queryset = AbstractUser.objects.filter()
        data = serializers.serialize("json", queryset)
        try:
            f = open(f"tests/fixtures/json/AbstractUser.json", "w")
            f.write(data)
        except Exception as exp:    
            logger.warning(repr(exp))
        finally:
            f.close()
            
    async def handle(self, *args, **kwargs):
        await self.generate_data()

