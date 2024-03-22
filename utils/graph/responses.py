# Third-party Libraries
import strawberry

# Own Libraries
from utils.graph.enums import ResponseCodeEnum
from utils.graph.interfaces import ResponseError


@strawberry.type
class ResponseValidationError(ResponseError):
    value: strawberry.Private[object] = ResponseCodeEnum.VALIDATION_ERROR.value
    default_message = f"{value} - There was an error"

    @strawberry.field()
    def code(self) -> str:
        return self.value

    @strawberry.field(name="message")
    def custom_message(self) -> str:
        return self.message or self.default_message


@strawberry.type
class ResponseIntegrityError(ResponseError):
    value: strawberry.Private[object] = ResponseCodeEnum.INTEGRITY_ERROR.value
    default_message = f"{value} - There was an error"

    @strawberry.field()
    def code(self) -> str:
        return self.value

    @strawberry.field(name="message")
    def custom_message(self) -> str:
        return self.message or self.default_message


@strawberry.type
class ResponseInternalError(ResponseError):
    value: strawberry.Private[object] = ResponseCodeEnum.INTERNAL_ERROR.value
    default_message = f"{value} - There was an error"

    @strawberry.field()
    def code(self) -> str:
        return self.value

    @strawberry.field(name="message")
    def custom_message(self) -> str:
        return self.message or self.default_message


DEFAULT_ERROR_TYPES = (
    ResponseValidationError,
    ResponseIntegrityError,
    ResponseInternalError,
)
