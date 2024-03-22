# Third-party Libraries
from django.contrib import admin

# Own Libraries
from apps.core.models import UserZone, Zone


class UserZoneInlineAdmin(admin.TabularInline):
    model = UserZone
    extra = 0
    fields = (
        "zone",
        "is_active",
        "is_deleted",
    )
    raw_id_fields = ("zone",)
    verbose_name_plural = "Barrios"


@admin.register(Zone)
class ZoneAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "city", "is_active")
