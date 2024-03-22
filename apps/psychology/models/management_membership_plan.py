# Third-party Libraries
from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone

# Own Libraries
from apps.psychology import psychology_constants
from utils.models import AuditableMixin

User = get_user_model()


def default_membership_options():
    return dict(
        items=[],
        modalidad="",
    )


class Membership(AuditableMixin):
    alias = models.CharField(max_length=255)
    membership_plan = models.SmallIntegerField(
        choices=psychology_constants.MEMBERSHIP_PLAN_TYPE_CHOICES,
        default=psychology_constants.BASIC_PLAN,
        db_index=True,
        help_text="Membership plan",
    )

    def __str__(self):
        return self.alias

    class Meta:
        verbose_name = "Plan"
        verbose_name_plural = "Planes"


class MembershipPrice(AuditableMixin):
    membership = models.ForeignKey(
        "Membership",
        on_delete=models.PROTECT,
        blank=True,
        null=True,
    )
    price = models.FloatField(default=0)
    promotional_price = models.FloatField(default=0)
    membership_options = models.JSONField(
        default=default_membership_options,
        blank=True,
        null=True,
    )
    created_by = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name="membership_price_created_set",
    )
    edited_by = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name="membership_price_edited_set",
    )

    def __str__(self):
        return f"{self.membership.alias}"

    class Meta:
        verbose_name = "Precio del plan"
        verbose_name_plural = "Precios por planes"

    @staticmethod
    def inactive_membership_plans(**kwargs):
        objs = MembershipPrice.objects.filter(is_active=True, **kwargs)
        if objs.exists():
            objs.update(is_active=False, is_deleted=True)

    def save(self, *args, **kwargs):
        if not self.pk:
            self.inactive_membership_plans(membership=self.membership)

        save_instance = super().save(*args, **kwargs)

        if self.pk:
            HistoryMembershipPrice.create_registers(
                membership_price=self,
                new_price=self.price,
            )
        return save_instance


class HistoryMembershipPrice(AuditableMixin):
    membership_price = models.ForeignKey(
        "MembershipPrice",
        on_delete=models.PROTECT,
        related_name="history_membership_price_set",
    )
    price = models.FloatField(default=0)

    def __str__(self):
        return f"{self.membership_price}"

    @classmethod
    def create_registers(
        cls,
        membership_price: MembershipPrice,
        new_price: float = 0.0,
    ):
        kwargs = dict(
            membership_price=membership_price, is_active=True, is_deleted=False
        )

        previous_results = cls.objects.filter(**kwargs).order_by("-created_at")

        if not previous_results.exists():
            return cls.objects.create(
                membership_price=membership_price, price=new_price
            )
        last_result = previous_results.first()
        if last_result.price != new_price:
            last_result.is_active = False
            last_result.updated_at = timezone.now()
            last_result.save(update_fields=["is_active", "updated_at"])

            return cls.objects.create(
                membership_price=membership_price, price=new_price
            )
        return last_result
