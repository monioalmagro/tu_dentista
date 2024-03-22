# Third-party Libraries
from django.contrib.auth import get_user_model
from django.db import models

# Own Libraries
from utils.models import AuditableMixin, SlugMixin

User = get_user_model()


class Language(AuditableMixin, SlugMixin):
    flag_icon = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self) -> str:
        return f"{self.slug}"

    class Meta:
        verbose_name = "Idioma"
        verbose_name_plural = "Idiomas"


class UserLanguage(AuditableMixin):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="user_language_set",
    )
    language = models.ForeignKey(
        "Language",
        on_delete=models.PROTECT,
        related_name="user_language_set",
        blank=True,
        null=True,
    )

    def __str__(self):
        return f"{self.user.username} ({self.language})"

    class Meta:
        verbose_name = "Idioma de usuario"
        verbose_name_plural = "Idiomas de los usuarios"
        constraints = [
            models.UniqueConstraint(
                fields=["user", "language"],
                name="unique language for user",
            )
        ]
