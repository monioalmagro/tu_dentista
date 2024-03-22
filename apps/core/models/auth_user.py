# Third-party Libraries
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

# Own Libraries
from apps.core import core_constants
from apps.psychology import psychology_constants
from config.enviroment_vars import settings


class AuthUser(AbstractUser):
    email = models.EmailField(_("email address"), unique=True, db_index=True)
    username = models.CharField(
        _("username"),
        max_length=100,
        blank=True,
        unique=True,
        db_index=True,
    )
    first_name = models.CharField(_("first name"), max_length=30, blank=True)
    last_name = models.CharField(_("last name"), max_length=30, blank=True)
    date_joined = models.DateTimeField(_("date joined"), auto_now_add=True)
    is_active = models.BooleanField(_("active"), default=True)
    nro_dni = models.CharField(
        max_length=25,
        blank=True,
        null=True,
        unique=True,
        db_index=True,
    )
    nro_matricula = models.CharField(
        max_length=25,
        blank=True,
        null=True,
        unique=True,
        db_index=True,
    )
    cuit = models.CharField(
        max_length=25,
        blank=True,
        null=True,
        unique=True,
        db_index=True,
    )
    phone = models.CharField(
        max_length=30,
        blank=True,
        null=True,
    )
    gender = models.SmallIntegerField(
        choices=core_constants.GENDER_CHOICES,
        db_index=True,
        blank=True,
        null=True,
    )
    facebook_profile = models.URLField(
        blank=True,
        null=True,
        unique=True,
        verbose_name="Facebook",
    )
    instagram_profile = models.URLField(
        blank=True,
        null=True,
        unique=True,
        verbose_name="Instagram",
    )
    linkedin_profile = models.URLField(
        blank=True,
        null=True,
        unique=True,
        verbose_name="LinkedIn",
    )
    is_verified_profile = models.BooleanField(default=False)
    verified_profile_at = models.DateTimeField(blank=True, null=True)
    personal_address = models.TextField(blank=True, null=True)

    attention_schedule = models.CharField(max_length=50, blank=True, null=True)
    membership_plan = models.SmallIntegerField(
        choices=psychology_constants.MEMBERSHIP_PLAN_TYPE_CHOICES,
        default=psychology_constants.BASIC_PLAN,
        db_index=True,
        blank=True,
        null=True,
        help_text="Membership plan",
    )

    def __str__(self):
        _name = self.username or self.email
        return f"{_name}"

    def save(self, *args, **kwargs):
        self.verified_profile_at = timezone.now() if self.is_verified_profile else None
        super().save(*args, **kwargs)

    @property
    def default_profile_picture(self):
        _decires_url = settings.DECIRES_URL
        _static_url = settings.STATIC_URL
        _base_url = f"{_decires_url}{_static_url}"
        if self.gender == 2:
            return f"{_base_url}{settings.DEFAULT_THUMBNAIL_FEMALE_IMAGE}"
        return f"{_base_url}{settings.DEFAULT_THUMBNAIL_MALE_IMAGE}"

    @property
    def profile_url(self) -> str:
        return reverse("core:professional:retrieve", kwargs={"pk": self.pk})
