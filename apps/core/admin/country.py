# Third-party Libraries
from django.contrib import admin

# Own Libraries
from apps.core.models import Country


@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "is_active")
