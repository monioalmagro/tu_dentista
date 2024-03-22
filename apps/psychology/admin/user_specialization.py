# Third-party Libraries
from django.contrib import admin
from django.http.request import HttpRequest

# Own Libraries
from apps.psychology.models import UserSpecialization


class UserSpecializationInline(admin.TabularInline):
    model = UserSpecialization
    verbose_name_plural = "Especializaciones"
    fields = (
        "specialization",
        "is_active",
        "is_deleted",
    )
    raw_id_fields = (
        "specialization",
        "user",
    )
    extra = 0

    # def has_add_permission(self, request: HttpRequest, obj=None) -> bool:
    #     return False

    def has_change_permission(self, request: HttpRequest, obj=None) -> bool:
        return False

    def has_delete_permission(self, request: HttpRequest, obj=None) -> bool:
        return False
