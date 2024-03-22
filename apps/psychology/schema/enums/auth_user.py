# Standard Libraries
import enum

# Third-party Libraries
import strawberry

# Own Libraries
from apps.core import core_constants
from apps.psychology import psychology_constants


@strawberry.enum()
class AuthUserGenderEnum(enum.Enum):
    MASCULINO = strawberry.enum_value(value=core_constants.HOMBRE)
    FEMENINO = strawberry.enum_value(value=core_constants.MUJER)


@strawberry.enum()
class AuthUserMembershipPlanEnum(enum.Enum):
    BASICO = strawberry.enum_value(value=psychology_constants.BASIC_PLAN)
    PREMIUM = strawberry.enum_value(value=psychology_constants.PREMIUM_PLAN)
    VIP = strawberry.enum_value(value=psychology_constants.VIP_PLAN)
