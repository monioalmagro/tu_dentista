# Third-party Libraries
from django.db import models

# Own Libraries
from utils.models import AuditableMixin, SlugMixin


class City(AuditableMixin, SlugMixin):
    country = models.ForeignKey(
        "Country",
        on_delete=models.CASCADE,
        related_name="city_set",
    )

    def __str__(self) -> str:
        return f"{self.name}"

    class Meta:
        verbose_name = "Ciudad"
        verbose_name_plural = "Ciudades"
