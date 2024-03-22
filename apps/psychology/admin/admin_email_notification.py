# Third-party Libraries
from django.contrib import admin
from django.http.request import HttpRequest
from django.urls import reverse
from django.utils.html import format_html

# Own Libraries
from apps.psychology import psychology_constants
from apps.psychology.models import AdminEmailNotification


@admin.register(AdminEmailNotification)
class AdminEmailNotificationAdmin(admin.ModelAdmin):
    list_display = (
        "content_type",
        "object_id",
        "admin_email",
        "was_reported",
        "seen_notification",
        "object_link",
        "is_active",
        "is_deleted",
    )
    list_editable = ("was_reported",)
    readonly_fields = ("object_link",)

    @admin.display(description="Link relacionado")
    def object_link(self, obj):
        if obj.content_type == psychology_constants.CONTACT_ME:
            url = reverse("admin:psychology_contactme_change", args=[obj.object_id])
            model = "mensaje"
        else:
            url = reverse("admin:psychology_userpayment_change", args=[obj.object_id])
            model = "pago"
        return format_html('<a href="{}">Ver {}</a>', url, model)

    def has_add_permission(self, request: HttpRequest, obj=None) -> bool:
        return False

    def has_change_permission(self, request: HttpRequest, obj=None) -> bool:
        return False

    def has_delete_permission(self, request: HttpRequest, obj=None) -> bool:
        return False
