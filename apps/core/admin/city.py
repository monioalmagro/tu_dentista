# Third-party Libraries
from django.contrib import admin

# Own Libraries
from apps.core.models import City


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "country", "is_active")
