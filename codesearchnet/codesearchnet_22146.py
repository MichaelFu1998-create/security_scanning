def frictional_resistance_coef(length, speed, **kwargs):
    """
    Flat plate frictional resistance of the ship according to ITTC formula.
    ref: https://ittc.info/media/2021/75-02-02-02.pdf

    :param length: metres length of the vehicle
    :param speed: m/s speed of the vehicle
    :param kwargs: optional could take in temperature to take account change of water property
    :return: Frictional resistance coefficient of the vehicle
    """
    Cf = 0.075 / (np.log10(reynolds_number(length, speed, **kwargs)) - 2) ** 2
    return Cf