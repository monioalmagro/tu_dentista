# Third-party Libraries
from django.db import models

# Own Libraries
from utils.models import AuditableMixin, SlugMixin


class Country(AuditableMixin, SlugMixin):
    code = models.CharField(max_length=150)

    def __str__(self) -> str:
        return f"{self.name}"

    class Meta:
        verbose_name = "País"
        verbose_name_plural = "Paises"
