def reynolds_number(length, speed, temperature=25):
    """
    Reynold number utility function that return Reynold number for vehicle at specific length and speed.
    Optionally, it can also take account of temperature effect of sea water.

        Kinematic viscosity from: http://web.mit.edu/seawater/2017_MIT_Seawater_Property_Tables_r2.pdf

    :param length: metres length of the vehicle
    :param speed: m/s speed of the vehicle
    :param temperature: degree C 
    :return: Reynolds number of the vehicle (dimensionless)
    """
    kinematic_viscosity = interpolate.interp1d([0, 10, 20, 25, 30, 40],
                                               np.array([18.54, 13.60, 10.50, 9.37, 8.42, 6.95]) / 10 ** 7)
    # Data from http://web.mit.edu/seawater/2017_MIT_Seawater_Property_Tables_r2.pdf
    Re = length * speed / kinematic_viscosity(temperature)
    return Re