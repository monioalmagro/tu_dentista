# Standard Libraries
import functools
import logging

# Third-party Libraries
from django.db import DatabaseError, IntegrityError
from pydantic import ValidationError

# Own Libraries
from utils.graph.responses import (
    ResponseIntegrityError,
    ResponseInternalError,
    ResponseValidationError,
)

logger = logging.getLogger(__name__)


async def pydantic_error_handler(exp: ValidationError) -> str:
    """
    Decode Pydantic ValidationError and extract detailed error messages.

    Parameters:
    - exp (ValidationError): Pydantic ValidationError instance.

    Returns:
    str: A formatted string containing detailed error messages.
    """
    try:
        field_errors = exp.errors()
        error_messages = [
            f"{field['loc'][0]}: {field['msg']}" for field in field_errors
        ]
        return ", ".join(error_messages)
    except Exception as e:
        logger.error(f"Error in pydantic_error_handler: {str(e)}")
        return "Error decoding Pydantic error message"


def mutation_exception_handler(log_tag: str):
    """
    Decorator that handles specific exceptions for asynchronous
    functions in Django.

    Parameters:
    - log_tag (str): Log tag used to identify log entries.

    Usage:
    @mutation_exception_handler("my_log_tag")
    async def my_async_function():
        # ...
    """

    def decorator(func):
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            if not isinstance(log_tag, str):
                raise ValueError("log_tag debe ser una cadena")
            full_log_tag = f"{log_tag}.{func.__name__}"
            try:
                result = await func(*args, **kwargs)
                return result
            except (AssertionError, ValidationError) as exp:
                if isinstance(exp, ValidationError):
                    message = await pydantic_error_handler(exp)
                else:
                    message = str(exp)

                logger.warning(
                    f"*** {full_log_tag}, VALIDATION ERROR"
                    f" {str(exp)} - {repr(exp)}***",
                    exc_info=True,
                )
                return ResponseValidationError(message=str(message))
            except (DatabaseError, IntegrityError) as exp:
                logger.warning(
                    f"*** {full_log_tag}, INTEGRITY ERROR"
                    f" {str(exp)} - {repr(exp)}***",
                    exc_info=True,
                )
                return ResponseIntegrityError(message=str(exp))
            except Exception as exp:
                logger.warning(
                    f"*** {full_log_tag}, INTERNAL ERROR"
                    f" {str(exp)} - {repr(exp)}***",
                    exc_info=True,
                )
                return ResponseInternalError(message=str(exp))

        return wrapper

    return decorator
