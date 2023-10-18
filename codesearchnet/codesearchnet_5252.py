def get_platform_pwm(**keywords):
    """Attempt to return a PWM instance for the platform which the code is being
    executed on.  Currently supports only the Raspberry Pi using the RPi.GPIO
    library and Beaglebone Black using the Adafruit_BBIO library.  Will throw an
    exception if a PWM instance can't be created for the current platform.  The
    returned PWM object has the same interface as the RPi_PWM_Adapter and
    BBIO_PWM_Adapter classes.
    """
    plat = Platform.platform_detect()
    if plat == Platform.RASPBERRY_PI:
        import RPi.GPIO
        return RPi_PWM_Adapter(RPi.GPIO, **keywords)
    elif plat == Platform.BEAGLEBONE_BLACK:
        import Adafruit_BBIO.PWM
        return BBIO_PWM_Adapter(Adafruit_BBIO.PWM, **keywords)
    elif plat == Platform.UNKNOWN:
        raise RuntimeError('Could not determine platform.')