# Standard Libraries
from abc import ABC, abstractmethod
from typing import Type, TypeVar

# Third-party Libraries
from pydantic import BaseModel
from strawberry.types import Info

_PydanticValidator = TypeVar("_PydanticValidator", bound=BaseModel)


class BaseValidator(ABC):
    def __init__(self, _input: Type[_PydanticValidator]):
        self.input = _input

    @abstractmethod
    async def validation_controller(self):
        pass


class BaseMutationProcess(ABC):
    def __init__(self, validator_instance: Type[BaseValidator]):
        self.validator = validator_instance

    @abstractmethod
    async def action(self, info: Info | None = None):
        pass
