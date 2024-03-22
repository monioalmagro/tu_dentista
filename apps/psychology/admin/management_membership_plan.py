# Standard Libraries
from typing import Any

# Third-party Libraries
from django.contrib import admin
from django.http import HttpRequest

# Own Libraries
from apps.psychology.models import (
    HistoryMembershipPrice,
    Membership,
    MembershipPrice,
)


@admin.register(Membership)
class MembershipAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "alias",
        "membership_plan",
        "is_active",
        "is_deleted",
    )


class HistoryMembershipPriceInlineAdmin(admin.TabularInline):
    model = HistoryMembershipPrice
    fields = (
        "id",
        "price",
        "is_active",
        "created_at",
    )
    extra = 0
    raw_id_fields = ("membership_price",)
    readonly_fields = ("created_at",)
    ordering = ["-created_at"]

    def has_add_permission(self, request: HttpRequest, obj=None) -> bool:
        return False

    def has_change_permission(self, request: HttpRequest, obj=None) -> bool:
        return False

    def has_delete_permission(self, request: HttpRequest, obj=None) -> bool:
        return False


@admin.register(MembershipPrice)
class MembershipPriceAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "membership",
        "created_by",
        "price",
        "promotional_price",
        "is_active",
        # "created_at",
        "updated_at",
        "is_deleted",
    )
    raw_id_fields = ("created_by", "edited_by", "membership")

    readonly_fields = (
        # "created_at",
        "created_by",
        "edited_by",
        "updated_at",
    )
    inlines = (HistoryMembershipPriceInlineAdmin,)

    def save_model(self, request: Any, obj: Any, form: Any, change: Any) -> None:
        if not obj.pk:
            obj.created_by = request.user
            obj.edited_by = request.user

            if change:
                obj.edited_by = request.user
        return super().save_model(request, obj, form, change)
