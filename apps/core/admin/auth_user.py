# Standard Libraries
import logging

# Third-party Libraries
from django.contrib import admin, messages
from django.contrib.auth.admin import UserAdmin
from django.utils import timezone

# Own Libraries
from apps.core.admin.zone import UserZoneInlineAdmin
from apps.core.models import AuthUser
from apps.psychology.admin import (
    ContactMeInline,
    UserAttachmentInLine,
    UserCarreerInline,
    UserLanguageInline,
    UserPaymentInline,
    UserSpecializationInline,
)

logger = logging.getLogger(__name__)


@admin.register(AuthUser)
class UserAdmin(UserAdmin):
    list_display = (
        "id",
        "username",
        "email",
        "get_was_paid",
        "is_active",
        "is_verified_profile",
    )
    inlines = [
        UserAttachmentInLine,
        UserZoneInlineAdmin,
        UserLanguageInline,
        UserCarreerInline,
        UserSpecializationInline,
        UserPaymentInline,
        ContactMeInline,
    ]

    fieldsets = (
        ("Usuario", {"fields": ("username",)}),
        (
            "Información personal",
            {
                "fields": (
                    "first_name",
                    "last_name",
                    "nro_dni",
                    "gender",
                ),
            },
        ),
        (
            "Información de Contacto",
            {
                "fields": (
                    "phone",
                    "email",
                    "personal_address",
                    "facebook_profile",
                    "instagram_profile",
                    "linkedin_profile",
                    "attention_schedule",
                ),
            },
        ),
        (
            "Información Profesional",
            {
                "fields": (
                    "nro_matricula",
                    "cuit",
                    "is_verified_profile",
                    "verified_profile_at",
                    "membership_plan",
                ),
            },
        ),
        (
            "Permisos",
            {
                "classes": ("collapse",),
                "fields": (
                    "is_superuser",
                    "is_staff",
                    "is_active",
                    "password",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        (
            "Auditoria",
            {
                "classes": ("collapse",),
                "fields": (
                    "date_joined",
                    "get_was_paid",
                    "last_login",
                ),
            },
        ),
    )

    search_fields = (
        "email",
        "nro_dni",
        "nro_matricula",
        "cuit",
        "first_name__icontains",
        "last_name__icontains",
    )
    list_filter = (
        "is_staff",
        "is_superuser",
        "is_verified_profile",
    )
    readonly_fields = (
        "date_joined",
        "last_login",
        "verified_profile_at",
        "get_was_paid",
    )
    # raw_id_fields = ("office_locations",)

    actions = [
        "verified_profile",
        "unverified_profile",
    ]

    @admin.display(description="Al día con el pago del sistema?")
    def get_was_paid(self, obj: AuthUser) -> str:
        now = timezone.now()
        current_month = now.month
        if obj.user_payment_set.filter(
            created_at__month=current_month,
            was_paid=True,
        ).exists():
            return "Si"
        return "No"

    @admin.display(description="Verificar perfiles")
    def verified_profile(self, request, queryset):
        model = self.model._meta.verbose_name
        _count = queryset.count()
        message = "A %(count)d %(model)s se les ha sido verificado sus perfiles." % {
            "count": _count,
            "model": model,
        }
        self.message_user(request, message, messages.SUCCESS)
        queryset.update(
            is_verified_profile=True,
            verified_profile_at=timezone.now(),
        )
        return queryset

    @admin.display(description="Remover la verificación de perfiles")
    def unverified_profile(self, request, queryset):
        model = self.model._meta.verbose_name
        _count = queryset.count()
        message = (
            "A %(count)d %(model)s se les ha sido removido la verificación de sus perfiles."
            % {
                "count": _count,
                "model": model,
            }
        )
        self.message_user(request, message, messages.SUCCESS)
        queryset.update(
            is_verified_profile=False,
            verified_profile_at=None,
        )
        return queryset

    # list_select_related = ()
    show_full_result_count = False
    actions_selection_counter = False
    ordering = ("id",)
