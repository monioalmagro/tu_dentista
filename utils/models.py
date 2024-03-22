# Standard Libraries
import logging

# Third-party Libraries
from django.db import connection, models
from django.utils.text import slugify

logger = logging.getLogger(__name__)


class AuditableMixin(models.Model):
    created_at: str = models.DateTimeField(
        auto_now_add=True,
        editable=False,
        verbose_name="Fecha de Creación",
    )
    updated_at: str = models.DateTimeField(
        auto_now=True,
        verbose_name="Fecha de modificación",
    )
    is_active: bool = models.BooleanField(
        default=True,
        db_index=True,
    )
    is_deleted: bool = models.BooleanField(
        default=False,
        db_index=True,
    )

    class Meta:
        abstract = True

    @classmethod
    def truncate(cls):
        """
        Truncate Table and Restart index.
        How to use:
        - cls.truncate()
        """
        try:
            db_table = cls._meta.db_table

            sql = f"TRUNCATE TABLE {db_table} RESTART IDENTITY CASCADE;"
            with connection.cursor() as cursor:
                cursor.execute(sql)
            logger.info(f"*** {db_table}.truncate table success!!! ***")
        except Exception as exp:
            error = str(exp)
            logger.error(
                f"***Error: {db_table}.truncate : {error} - {repr(exp)}***",
                exc_info=True,
            )


class SlugMixin(models.Model):
    name = models.CharField(max_length=150)
    slug = models.SlugField(blank=True, null=True, unique=True, db_index=True)

    class Meta:
        abstract = True

    def save(
        self,
        *args,
        **kwargs,
    ) -> None:
        if not self.pk or (not self.slug and self.name):
            self.slug = slugify(self.name)
        return super().save(
            *args,
            **kwargs,
        )
