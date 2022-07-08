"""Here are functions for converting temperature"""
from decimal import Decimal


class SpecialKeyError(Exception):
    """Custom exception for convert function"""

    def __init__(self, *args: object) -> None:
        super().__init__(*args)


def convert(number: Decimal, to: str, _from: str) -> Decimal:
    """number: Decimal --> This is temperature value that is going to be converted\n
    ---
    to: str --> "c", "f" or "k" (special key)\n
    ---
    _from: str --> "c", "f" or "k" (special key)\n
    ---
    Special keys:
    ---
    "c" --> Celsius\n
    "f" --> Fahrenheit\n
    "k" --> Kelvin\n
    ---
    Returns
    ---
    Decimal:
        temperature value after converting
    ---
    Raises:
    ---
    TypeError -> when any param is wrong type

    SpecialKeyError -> when wrong special key is entered"""
    # Check values:
    if not isinstance(number, Decimal):
        raise TypeError(
            f'Expected {Decimal} type for "number" but got -> "{type(number)}"'
        )
    if not isinstance(to, str):
        raise TypeError(f'Expected {str} type for "to" but got -> "{type(to)}"')
    if not isinstance(_from, str):
        raise TypeError(f'Expected {str} type for "_from" but got -> "{type(_from)}"')

    match to, _from:
        # When both keys are the same
        case "c", "c":
            return number
        case "f", "f":
            return number
        case "k", "k":
            return number
        # Normal conversion
        # Celsius to ____
        case "c", "f":
            return round((Decimal(number) - 32) * (Decimal(5) / Decimal(9)), 3)
        case "c", "k":
            return round((Decimal(number) - Decimal(273.15)), 3)
        # Fahrenheit to ____
        case "f", "c":
            return round(((Decimal(number) * (Decimal(9) / Decimal(5))) + 32), 3)
        case "f", "k":
            return round(
                ((Decimal(number) * (Decimal(9) / Decimal(5))) - Decimal(459.67)), 3
            )
        # Celsius to ____
        case "k", "f":
            return round(
                ((Decimal(number) + Decimal(459.67)) * (Decimal(5) / Decimal(9))), 3
            )
        case "k", "c":
            return round((Decimal(number) + Decimal(273.15)), 3)
        # More exceptions:
        case _, "c":
            raise SpecialKeyError(f'Wrong key is entered: "to" -> "{to}"')
        case _, "f":
            raise SpecialKeyError(f'Wrong key is entered: "to" -> "{to}"')
        case _, "k":
            raise SpecialKeyError(f'Wrong key is entered: "to" -> "{to}"')
        case "c", _:
            raise SpecialKeyError(f'Wrong key is entered: "_from" -> "{_from}"')
        case "f", _:
            raise SpecialKeyError(f'Wrong key is entered: "_from" -> "{_from}"')
        case "k", _:
            raise SpecialKeyError(f'Wrong key is entered: "_from" -> "{_from}"')
        case _:
            raise SpecialKeyError(
                f'All entered keys are wrong: "to" -> "{to}", "_from" -> "{_from}"'
            )
