# Third-party Libraries
from django.contrib.auth import get_user_model
from django.db import models

# Own Libraries
from config.enviroment_vars import settings
from utils.models import AuditableMixin
from utils.upload_files import upload_attachment_file

User = get_user_model()


class UserAttachment(AuditableMixin):
    USER_IMAGE = 1
    USER_DNI = 2
    USER_MATRICULA = 3

    SOURCE_CONTENT_TYPE_CHOICES = (
        (USER_IMAGE, "USER_IMAGE"),
        (USER_DNI, "USER_DNI"),
        (USER_MATRICULA, "USER_MATRICULA"),
    )
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255, null=True, blank=True)
    image = models.ImageField(
        upload_to=upload_attachment_file,
        # storage=storage_share_file,
        max_length=255,
        null=True,
        blank=True,
    )
    media_file = models.FileField(
        upload_to=upload_attachment_file,
        # storage=storage_share_file,
        max_length=255,
        null=True,
        blank=True,
    )
    source_content_type = models.SmallIntegerField(
        choices=SOURCE_CONTENT_TYPE_CHOICES,
        blank=True,
        null=True,
        db_index=True,
    )
    content_type = models.CharField(
        max_length=100,
        null=True,
        blank=True,
    )
    size = models.IntegerField(
        null=True,
        blank=True,
    )
    created_by = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name="user_attachment_created_by_set",
        null=True,
        blank=True,
    )
    updated_by = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name="user_attachment_updated_by_set",
        null=True,
        blank=True,
    )
    url_path = models.URLField(
        max_length=255,
        blank=True,
        null=True,
    )

    def __str__(self) -> str:
        return f"{self.name} ({self.content_type})"

    class Meta:
        verbose_name = "Archivo del usuario"
        verbose_name_plural = "Archivos de los usuarios"

    @property
    def url_content(self) -> str | None:
        if (base_media := settings.MEDIA_URL) and (
            url := self.image or self.media_file
        ):
            return f"{settings.DECIRES_URL}{base_media}{url}"
