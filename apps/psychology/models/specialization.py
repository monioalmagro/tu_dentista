# Third-party Libraries
from django.contrib.auth import get_user_model
from django.db import models

# Own Libraries
from utils.models import AuditableMixin

User = get_user_model()


class Specialization(AuditableMixin):
    name = models.CharField(max_length=150, unique=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name = "Especialización"
        verbose_name_plural = "Especializaciones"


class UserSpecialization(AuditableMixin):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="user_specialization_set",
    )
    specialization = models.ForeignKey(
        "Specialization",
        on_delete=models.PROTECT,
        related_name="user_specialization_set",
        blank=True,
        null=True,
    )

    def __str__(self):
        return f"{self.user.username} ({self.specialization})"

    class Meta:
        verbose_name = "Especialización del usuario "
        verbose_name_plural = "Especializaciones de los usuarios"
        constraints = [
            models.UniqueConstraint(
                fields=["user", "specialization"],
                name="unique specialization for user",
            )
        ]
