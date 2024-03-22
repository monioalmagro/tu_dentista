# Third-party Libraries
from django.db import models

# Own Libraries
from apps.psychology import psychology_constants
from utils.models import AuditableMixin


class AdminEmailNotification(AuditableMixin):
    object_id = models.IntegerField(db_index=True)
    content_type = models.SmallIntegerField(
        choices=psychology_constants.ADMIN_EMAIL_NOTIFICATION_CONTENT_TYPE_CHOICES,
        db_index=True,
    )
    admin_email = models.EmailField(max_length=254)
    was_reported = models.BooleanField(
        default=False,
        db_index=True,
    )
    seen_notification = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.admin_email}"

    class Meta:
        verbose_name = "Notificación de Email"
        verbose_name_plural = "Notificaciones de Email"
        constraints = [
            models.UniqueConstraint(
                fields=["object_id", "content_type"],
                name="unique notification for admin",
            )
        ]
