from typing import List

from sqlalchemy.dialects.postgresql import ENUM


def enum_joiner(enums: List[str]) -> str:
    if len(enums) == 2:
        return " or ".join(enums)

    if len(enums) > 2:
        return ", ".join(enums[:-1]) + f" or {enums[-1]}"

    return enums[0]


def enum_validator(
        field: str,
        value: str | None,
        enum: ENUM,
        required: bool = False
) -> str | None:
    if not required and value is None:
        return value

    options = enum.enums
    if value not in options:
        raise ValueError(
            f"The {field} possible options are {enum_joiner(options)}!"
        )

    return value
