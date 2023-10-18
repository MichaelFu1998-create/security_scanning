def froude_number(speed, length):
    """
    Froude number utility function that return Froude number for vehicle at specific length and speed.

    :param speed: m/s speed of the vehicle
    :param length: metres length of the vehicle
    :return: Froude number of the vehicle (dimensionless)
    """
    g = 9.80665  # conventional standard value m/s^2
    Fr = speed / np.sqrt(g * length)
    return Fr