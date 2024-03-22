# Standard Libraries
import logging
import os

# Third-party Libraries
from dotenv import load_dotenv
from pydantic import BaseSettings, Field, SecretStr

logger = logging.getLogger(__name__)
# Standard Libraries
import json

load_dotenv()


class AWSSettings(BaseSettings):
    AWS_REGION_NAME: str = Field(default="us-east-1", env="AWS_REGION_NAME")
    AWS_ACCESS_KEY_ID: str | None = Field(default=None, env="AWS_ACCESS_KEY_ID")
    AWS_SECRET_ACCESS_KEY: str | None = Field(default=None, env="AWS_SECRET_ACCESS_KEY")
    AWS_ACCOUNT_ID: int | None = Field(default=None, env="AWS_ACCOUNT_ID")
    AWS_STAGE: str = Field(default="qa", env="AWS_STAGE")
    AWS_S3_BUCKET_NAME: str | None = Field(default=None, env="AWS_S3_BUCKET_NAME")

    class Config:
        env_prefix = ""
        case_sensitive = False
        env_file = ".env"
        env_file_encoding = "utf-8"
        json_loads = json.loads


aws_settings = AWSSettings()


class EMAILSettings(BaseSettings):
    EMAIL_BACKEND: str = Field(
        default="django.core.mail.backends.smtp.EmailBackend",
        env="EMAIL_BACKEND",
    )
    EMAIL_HOST: str = Field(
        default="smtp.gmail.com",
        env="EMAIL_HOST",
    )
    EMAIL_PORT: int = Field(
        default=587,
        env="EMAIL_PORT",
    )
    EMAIL_USE_TLS: bool = Field(
        default=True,
        env="EMAIL_USE_TLS",
    )
    EMAIL_HOST_USER: str = Field(
        default="decirespsicologia@gmail.com",
        env="EMAIL_HOST_USER",
    )
    EMAIL_HOST_PASSWORD: SecretStr = Field(
        default="qryk iyiy aghr fesj",
        env="EMAIL_HOST_PASSWORD",
    )


email_settings = EMAILSettings()


class PsychologySettings(BaseSettings):
    COMPOSE_PROJECT_NAME: str = Field(
        default="psychology",
        env="COMPOSE_PROJECT_NAME",
    )
    DJANGO_SETTINGS_MODULE: str = Field(
        env="DJANGO_SETTINGS_MODULE",
        default="config.settings.base",
    )
    SECRET_KEY: SecretStr | None = Field(
        default="*",
        env="SECRET_KEY",
    )
    DEBUG: bool = Field(env="DEBUG", default=True)
    JWT_SECRET_KEY: SecretStr | None = Field(
        default="insecure-jwt-secret-key",
        env="JWT_SECRET_KEY",
    )
    DATABASE_URL: str | None = Field(
        default="postgresql://postgres:postgres@postgres:5432/psychology_db",
        env="DATABASE_URL",
    )
    DJANGO_ALLOW_ASYNC_UNSAFE: bool | None = Field(
        default=True,
        env="DJANGO_ALLOW_ASYNC_UNSAFE",
    )
    SITE_NAME: str = Field(env="SITE_NAME", default="Redpsidecires")
    DECIRES_URL: str = Field(
        env="DECIRES_URL",
        default="http://localhost:8000",
    )
    GRAPHQL_URL: str = Field(
        env="GRAPHQL_URL",
        default="http://localhost:9000/api/graph/psychology/",
    )
    MEDIA_URL: str | None = Field(default="/media/")
    STATIC_URL: str | None = Field(default="/static/")
    DECIRES_EMAIL: str = Field(
        default="decirespsicologia@gmail.com", env="DECIRES_EMAIL"
    )
    DEFAULT_THUMBNAIL_FEMALE_IMAGE: str = Field(
        default="assets/img/user/female_user.jpg"
    )
    DEFAULT_THUMBNAIL_MALE_IMAGE: str = Field(default="assets/img/user/male_user.jpg")
    AWS_SETTINGS: AWSSettings | None = aws_settings
    EMAIL_SETTINGS: EMAILSettings | None = email_settings
    ALLOWED_HOSTS: list[str] = Field(default=[], env="ALLOWED_HOSTS")

    PASSWORD_DEFAULT: SecretStr = Field(default="Av123456789#")
    CORS_ALLOWED_ORIGINS: list[str] = Field(default=[], env="CORS_ALLOWED_ORIGINS")
    CSRF_TRUSTED_ORIGINS: list[str] = Field(default=[], env="CSRF_TRUSTED_ORIGINS")

    class Config:
        env_prefix = ""
        case_sensitive = False
        env_file = ".env"
        env_file_encoding = "utf-8"
        json_loads = json.loads

        @classmethod
        def parse_env_var(cls, field_name: str, raw_val: str):
            if field_name == "ALLOWED_HOSTS":
                return os.environ.get("ALLOWED_HOSTS", "*").split(",")
            if field_name == "CORS_ALLOWED_ORIGINS":
                return os.environ.get("CORS_ALLOWED_ORIGINS", "*").split(",")
            if field_name == "CSRF_TRUSTED_ORIGINS":
                return os.environ.get("CSRF_TRUSTED_ORIGINS", "*").split(",")
            return cls.json_loads(raw_val)


settings = PsychologySettings()
