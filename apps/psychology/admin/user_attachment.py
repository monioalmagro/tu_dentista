# Third-party Libraries
from django.contrib import admin

# Own Libraries
from apps.psychology.models import UserAttachment


class UserAttachmentInLine(admin.TabularInline):
    model = UserAttachment
    verbose_name_plural = "Archivos Adjuntos"
    fields = (
        "name",
        "description",
        "source_content_type",
        "content_type",
        "media_file",
        "image",
        "is_active",
        "is_deleted",
    )
    extra = 0
    raw_id_fields = (
        "created_by",
        "updated_by",
    )
    fk_name = "created_by"

    # def has_add_permission(self, request: HttpRequest, obj=None) -> bool:
    #     return False

    # def has_change_permission(self, request: HttpRequest, obj=None) -> bool:
    #     return False

    # def has_delete_permission(self, request: HttpRequest, obj=None) -> bool:
    #     return False


@admin.register(UserAttachment)
class UserAttachmentAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "description",
        "content_type",
        "media_file",
        "image",
        "created_by",
        "is_active",
        "is_deleted",
    )
    raw_id_fields = (
        "created_by",
        "updated_by",
    )
