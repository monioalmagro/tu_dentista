# Standard Libraries
import enum

# Third-party Libraries
import strawberry

# Own Libraries
from apps.core import core_constants


@strawberry.enum()
class SourceAttachmentContentTypeEnum(enum.Enum):
    USER_IMAGE_PROFILE = strawberry.enum_value(value=core_constants.USER_IMAGE)
    USER_DNI = strawberry.enum_value(value=core_constants.USER_DNI)
    USER_MATRICULA = strawberry.enum_value(value=core_constants.USER_MATRICULA)
