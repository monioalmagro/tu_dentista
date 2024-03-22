# Standard Libraries
from typing import Optional

# Third-party Libraries
import strawberry

# Own Libraries
from utils.graph.enums import ErrorTypesEnum


@strawberry.type
class Response:
    code: str
    type: str
    message: Optional[str] = ""


@strawberry.type
class ResponseError(Response):
    @strawberry.field
    def type(self) -> str:
        if self.__class__.__name__ in (
            "ResponseValidationError",
            "ResponseIntegrityError",
            "ResponseInternalError",
        ):
            return ErrorTypesEnum.DEFAULT_ERROR.value
        return ErrorTypesEnum.CUSTOM_ERROR.value
