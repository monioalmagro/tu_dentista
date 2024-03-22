# Standard Libraries
import enum
from typing import Optional, Type, TypeVar

TEnum = TypeVar("TEnum", bound=enum.Enum)


def get_enum_instance_by_value(
    enum_class: Type[TEnum],
    value: int,
) -> Optional[TEnum]:
    """
    Get an instance of an enumeration by its integer value.

    Args:
        enum_class (Type[TEnum]): The enumeration class.
        value (int): The integer value to match.

    Returns:
        Optional[TEnum]: The enumeration instance if found, else None.
    """
    # Use filter to find the instance with matching value
    matching_enums = filter(lambda enum: enum.value == value, enum_class)

    # Use next to get the first matching instance or None if no match
    match = next(matching_enums, None)

    return match
