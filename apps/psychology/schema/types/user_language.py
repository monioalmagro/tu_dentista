# Third-party Libraries
import strawberry

# Own Libraries
from apps.psychology.models import Language, UserLanguage


@strawberry.type()
class LanguageSelect2Type:
    id: strawberry.ID
    text: str

    @classmethod
    def from_db_model(cls, instance: Language) -> "LanguageSelect2Type":
        return cls(
            id=instance.pk,
            text=instance.name,
        )


@strawberry.type()
class LanguageType:
    name: str | None = None
    slug: str | None = None
    flag_icon: str | None = None

    @classmethod
    def from_db_model(cls, instance: Language) -> "LanguageType":
        return cls(
            name=instance.name,
            slug=instance.slug,
            flag_icon=instance.flag_icon,
        )


@strawberry.type()
class UserLanguageType:
    language: LanguageType | None = None
    is_active: bool | None = None

    @classmethod
    def from_db_model(cls, instance: UserLanguage) -> "UserLanguageType":
        return cls(
            language=LanguageType.from_db_model(instance=instance.language),
            is_active=instance.is_active,
        )
