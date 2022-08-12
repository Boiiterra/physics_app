from decimal import Decimal


def iso_baric(
    temperature_1: int | Decimal,
    volume_1: int | Decimal,
    temperature_2: int | Decimal = False,
    volume_2: int | Decimal = False,
):
    """temperature_1 is mandatory\n
    volume_1 is mandatory\n
    temperature_2 or volume_2 must be entered (not both)\n
    Uses formula V/T=const\n
    returns value of temperature_2 or volume_2 based on which is not entered"""

    if temperature_2:
        return (temperature_2 * volume_1) / temperature_1
    elif volume_2:
        return (temperature_1 * volume_2) / volume_1
    else:
        raise Exception("You need to enter either temperature_2 or volume_2")


def iso_choric(
    pressure_1: int | Decimal,
    temperature_1: int | Decimal,
    pressure_2: int | Decimal = False,
    temperature_2: int | Decimal = False,
):
    """pressure_1 is mandatory\n
    temperature_1 is mandatory\n
    pressure_2 or temperature_2 must be entered (not both)\n
    Uses formula p/T=const\n
    returns value of pressure_2 or temperature_2 based on which is not entered"""

    if pressure_2:
        return (pressure_2 * temperature_1) / pressure_1
    elif temperature_2:
        return (pressure_1 * temperature_2) / temperature_1
    else:
        raise Exception("You need to enter either pressure_2 or temperature_2")


def iso_therm(
    pressure_1: int | Decimal,
    volume_1: int | Decimal,
    pressure_2: int | Decimal = False,
    volume_2: int | Decimal = False,
):
    """pressure_1 is mandatory\n
    volume_1 is mandatory\n
    pressure_2 or volume_2 must be entered (not both)\n
    Uses formula pV=const\n
    returns value of pressure_2 or volume_2 based on which is not entered"""

    if pressure_2:
        return (pressure_1 * volume_1) / pressure_2
    elif volume_2:
        return (pressure_1 * volume_1) / volume_2
    else:
        raise Exception("You need to enter either pressure_2 or volume_2")


def adiabatic():
    return


def polytrophic():
    return