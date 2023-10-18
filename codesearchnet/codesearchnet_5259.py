def platform_detect():
    """Detect if running on the Raspberry Pi or Beaglebone Black and return the
    platform type.  Will return RASPBERRY_PI, BEAGLEBONE_BLACK, or UNKNOWN."""
    # Handle Raspberry Pi
    pi = pi_version()
    if pi is not None:
        return RASPBERRY_PI

    # Handle Beaglebone Black
    # TODO: Check the Beaglebone Black /proc/cpuinfo value instead of reading
    # the platform.
    plat = platform.platform()
    if plat.lower().find('armv7l-with-debian') > -1:
        return BEAGLEBONE_BLACK
    elif plat.lower().find('armv7l-with-ubuntu') > -1:
        return BEAGLEBONE_BLACK
    elif plat.lower().find('armv7l-with-glibc2.4') > -1:
        return BEAGLEBONE_BLACK
    elif plat.lower().find('tegra-aarch64-with-ubuntu') > -1:
        return JETSON_NANO
        
    # Handle Minnowboard
    # Assumption is that mraa is installed
    try: 
        import mraa 
        if mraa.getPlatformName()=='MinnowBoard MAX':
            return MINNOWBOARD
    except ImportError:
        pass
    
    # Couldn't figure out the platform, just return unknown.
    return UNKNOWN