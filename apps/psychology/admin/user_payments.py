# Third-party Libraries
from django.contrib import admin

# Own Libraries
from apps.psychology.models import UserPayment


class UserPaymentInline(admin.TabularInline):
    model = UserPayment
    verbose_name_plural = "Pagos"
    fields = (
        "was_paid",
        "type",
        "membership_plan",
        "month",
        "observations",
        "created_at",
    )

    readonly_fields = (
        "created_at",
        "month",
    )
    extra = 0


@admin.register(UserPayment)
class UserPaymentAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "type",
        "membership_plan",
        "was_reported",
    )
    list_editable = ("was_reported",)
    raw_id_fields = ("user",)
