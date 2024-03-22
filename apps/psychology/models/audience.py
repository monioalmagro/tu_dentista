# Third-party Libraries
from django.db import models

# Own Libraries
from utils.models import AuditableMixin


class Audience(AuditableMixin):
    name = models.CharField(max_length=50)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name = "Audiencia"
        verbose_name_plural = "Audiencias"
