# Third-party Libraries
from django.contrib import admin

# Own Libraries
from apps.psychology.models import Specialization


class SpecializationInline(admin.TabularInline):
    model = Specialization
    fields = (
        "name",
        "description",
        "is_active",
    )


@admin.register(Specialization)
class SpecializationAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "description",
        "is_active",
        "is_deleted",
    )
