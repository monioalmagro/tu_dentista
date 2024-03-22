# Third-party Libraries
from django.contrib.auth import get_user_model
from django.db import models

# Own Libraries
from apps.psychology import psychology_constants
from utils.models import AuditableMixin

User = get_user_model()


class UserPayment(AuditableMixin):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="user_payment_set",
    )
    type = models.SmallIntegerField(
        choices=psychology_constants.PAYMENT_CHOICES,
        default=psychology_constants.MONTHLY_PAYMENT,
        db_index=True,
        blank=True,
        null=True,
    )
    membership_plan = models.SmallIntegerField(
        choices=psychology_constants.MEMBERSHIP_PLAN_TYPE_CHOICES,
        default=psychology_constants.BASIC_PLAN,
        db_index=True,
        blank=True,
        null=True,
        help_text="Membership plan",
    )
    was_paid = models.BooleanField(default=False, db_index=True)
    was_reported = models.BooleanField(default=False, db_index=True)
    observations = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = "Pago del usuario"
        verbose_name_plural = "Pagos de los usuarios"

    def __str__(self):
        return f"{self.was_paid}"

    @property
    def month(self) -> int:
        if self.created_at:
            return getattr(self.created_at, "month", "None")
