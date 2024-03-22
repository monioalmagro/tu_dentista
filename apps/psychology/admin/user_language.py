# Third-party Libraries
from django.contrib import admin

# Own Libraries
from apps.psychology.models import Language, UserLanguage


@admin.register(Language)
class LanguageAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "slug",
    )


class UserLanguageInline(admin.TabularInline):
    model = UserLanguage
    verbose_name_plural = "Idiomas"
    fields = (
        "language",
        "is_active",
        "is_deleted",
    )
    raw_id_fields = ("language",)
    extra = 0

    # def has_add_permission(self, request: HttpRequest, obj=None) -> bool:
    #     return False

    # def has_change_permission(self, request: HttpRequest, obj=None) -> bool:
    #     return False

    # def has_delete_permission(self, request: HttpRequest, obj=None) -> bool:
    #     return False
