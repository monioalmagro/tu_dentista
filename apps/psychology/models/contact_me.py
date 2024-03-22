# Third-party Libraries
from django.db import models
from django.utils.translation import gettext_lazy as _

# Own Libraries
from utils.models import AuditableMixin


class ContactMe(AuditableMixin):
    user = models.ForeignKey(
        "core.AuthUser",
        on_delete=models.PROTECT,
        related_name="professional_contact_set",
        verbose_name="Professional",
        help_text="Professional",
    )
    full_name = models.CharField(max_length=50, help_text="Visitor[external]")
    email = models.EmailField(_("email address"), db_index=True, max_length=50)
    phone = models.CharField(
        max_length=30,
        db_index=True,
        blank=True,
        null=True,
    )
    message = models.TextField()
    was_reported = models.BooleanField(default=False, db_index=True)

    def __str__(self):
        return f"{self.full_name} ({self.email})"

    class Meta:
        verbose_name = "Derivaciôn"
        verbose_name_plural = "Derivaciones"
