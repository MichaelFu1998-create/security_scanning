def _finalise_result_(compound, value, mass):
    """
    Convert the value to its final form by unit conversions and multiplying
    by mass.

    :param compound: Compound object.
    :param value: [J/mol] Value to be finalised.
    :param mass: [kg] Mass of compound.

    :returns: [kWh] Finalised value.
    """

    result = value / 3.6E6  # J/x -> kWh/x
    result = result / compound.molar_mass  # x/mol -> x/kg
    result = result * mass  # x/kg -> x

    return result