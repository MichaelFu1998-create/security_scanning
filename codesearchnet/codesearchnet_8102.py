def SPI(ledtype=None, num=0, **kwargs):
    """Wrapper function for using SPI device drivers on systems like the
    Raspberry Pi and BeagleBone. This allows using any of the SPI drivers
    from a single entry point instead importing the driver for a specific
    LED type.

    Provides the same parameters of
    :py:class:`bibliopixel.drivers.SPI.SPIBase` as
    well as those below:

    :param ledtype: One of: LPD8806, WS2801, WS281X, or APA102
    """

    from ...project.types.ledtype import make
    if ledtype is None:
        raise ValueError('Must provide ledtype value!')
    ledtype = make(ledtype)

    if num == 0:
        raise ValueError('Must provide num value >0!')
    if ledtype not in SPI_DRIVERS.keys():
        raise ValueError('{} is not a valid LED type.'.format(ledtype))

    return SPI_DRIVERS[ledtype](num, **kwargs)