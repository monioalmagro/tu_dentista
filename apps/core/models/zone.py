# Third-party Libraries
from django.contrib.auth import get_user_model
from django.db import models

# Own Libraries
from utils.models import AuditableMixin, SlugMixin

User = get_user_model()


class Zone(AuditableMixin, SlugMixin):
    city = models.ForeignKey(
        "City",
        on_delete=models.CASCADE,
        related_name="zone_set",
    )

    def __str__(self) -> str:
        return f"{self.name}"

    class Meta:
        verbose_name = "Barrio"
        verbose_name_plural = "Barrios"


class UserZone(AuditableMixin):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="user_zone_set",
    )
    zone = models.ForeignKey(
        "Zone",
        on_delete=models.PROTECT,
        related_name="user_zone_set",
        blank=True,
        null=True,
    )

    def __str__(self):
        return f"{self.user.username} ({self.zone})"

    class Meta:
        verbose_name = "Barrio del usuario"
        verbose_name_plural = "Barrios de los usuarios"
        constraints = [
            models.UniqueConstraint(
                fields=["user", "zone"],
                name="unique zone for user",
            )
        ]
