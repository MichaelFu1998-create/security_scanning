def get_platform_gpio(**keywords):
    """Attempt to return a GPIO instance for the platform which the code is being
    executed on.  Currently supports only the Raspberry Pi using the RPi.GPIO
    library and Beaglebone Black using the Adafruit_BBIO library.  Will throw an
    exception if a GPIO instance can't be created for the current platform.  The
    returned GPIO object is an instance of BaseGPIO.
    """
    plat = Platform.platform_detect()
    if plat == Platform.RASPBERRY_PI:
        import RPi.GPIO
        return RPiGPIOAdapter(RPi.GPIO, **keywords)
    elif plat == Platform.BEAGLEBONE_BLACK:
        import Adafruit_BBIO.GPIO
        return AdafruitBBIOAdapter(Adafruit_BBIO.GPIO, **keywords)
    elif plat == Platform.MINNOWBOARD:
        import mraa
        return AdafruitMinnowAdapter(mraa, **keywords)
    elif plat == Platform.JETSON_NANO:
        import Jetson.GPIO
        return RPiGPIOAdapter(Jetson.GPIO, **keywords)
    elif plat == Platform.UNKNOWN:
        raise RuntimeError('Could not determine platform.')