# Standard Libraries
# import re

# Third-party Libraries
import strawberry
from django.core.validators import validate_email
from pydantic import BaseModel, constr, validator


class ContactMePydanticModel(BaseModel):
    user_id: strawberry.ID
    full_name: str
    email: str
    phone: constr()
    message: str

    # @validator("phone")
    # @classmethod
    # def validate_phone(cls, value):
    #     pattern = r"^(?:\+\d{1,2} )?(?:(?:\(\d{1,4}\) \d{2}-\d{4})|(?:\d{1,4} \d{2}-\d{4})|(?:\d{1,4} \d{1,4} \d{2}-\d{4})|(?:\d{1,4} \d{1,4} \d{1,4} \d{2}-\d{4})|(?:\+\d{1,2} \d{1,2} \d{4} \d{2}-\d{4})|(?:\+\d{1,2} \d{1,4} \d{1,4} \d{2}-\d{4})|(?:\+\d{1,2} \d{1,4} \d{4} \d{2}-\d{4}))$"

    #     if not re.match(pattern, value):
    #         raise AssertionError(
    #             f"El número de teléfono {value} no cumple con el formato esperado."
    #         )

    #     return value

    @validator("email")
    @classmethod
    def email_check(cls, email):
        try:
            if len(email) == 0:
                raise AssertionError("Input email, invalid")
            # django validator
            validate_email(value=email)
        except Exception as exp:
            raise AssertionError(str(exp)) from exp
        return email

    @validator("message")
    @classmethod
    def validate_message(cls, value):
        _message = value.strip()
        if len(_message) < 1:
            raise AssertionError(
                "Mensaje vacio, este campo debe contener un texto válido."
            )
        elif len(_message) > 150:
            raise AssertionError(
                "El mensaje supera la cantidad de caracteres permitidos (150)."
            )
        return _message


@strawberry.experimental.pydantic.input(
    model=ContactMePydanticModel,
    all_fields=True,
)
class MutationContactMeInput:
    pass
