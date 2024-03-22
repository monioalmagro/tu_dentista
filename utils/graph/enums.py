# Standard Libraries
from enum import Enum

# Third-party Libraries
import strawberry


@strawberry.enum
class ResponseCodeEnum(Enum):
    VALIDATION_ERROR = strawberry.enum_value(value="4001_VALIDATION")
    INTEGRITY_ERROR = strawberry.enum_value(value="4002_INTEGRITY")
    INTERNAL_ERROR = strawberry.enum_value(value="4003_INTERNAL")


@strawberry.enum
class ErrorTypesEnum(Enum):
    DEFAULT_ERROR = strawberry.enum_value(value="ERROR")
    CUSTOM_ERROR = strawberry.enum_value(value="CUSTOM_ERROR")
