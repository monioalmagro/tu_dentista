# Third-party Libraries
from django.contrib import admin

# Own Libraries
from apps.psychology.models import Carreer


@admin.register(Carreer)
class CarreerAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "description",
        "is_active",
        "is_deleted",
    )
