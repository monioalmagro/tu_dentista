# Third-party Libraries
from django.contrib import admin

# Own Libraries
from apps.psychology.models import UserCarreer


class UserCarreerInline(admin.TabularInline):
    model = UserCarreer
    verbose_name_plural = "Titulaciones"
    fields = (
        "carreer",
        # "specializations",
        "service_method",
        "service_modality",
        "experience_summary",
        "is_active",
        "is_deleted",
    )
    raw_id_fields = (
        "carreer",
        # "specializations",
    )
    extra = 0


@admin.register(UserCarreer)
class UserCarreerAdmin(admin.ModelAdmin):
    list_display = ("user", "carreer", "is_active")
    raw_id_fields = (
        "user",
        "carreer",
        # "specializations",
    )
