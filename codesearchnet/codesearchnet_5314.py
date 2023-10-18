def require_repeated_start():
    """Enable repeated start conditions for I2C register reads.  This is the
    normal behavior for I2C, however on some platforms like the Raspberry Pi
    there are bugs which disable repeated starts unless explicitly enabled with
    this function.  See this thread for more details:
      http://www.raspberrypi.org/forums/viewtopic.php?f=44&t=15840
    """
    plat = Platform.platform_detect()
    if plat == Platform.RASPBERRY_PI and os.path.exists('/sys/module/i2c_bcm2708/parameters/combined'):
        # On the Raspberry Pi there is a bug where register reads don't send a
        # repeated start condition like the kernel smbus I2C driver functions
        # define.  As a workaround this bit in the BCM2708 driver sysfs tree can
        # be changed to enable I2C repeated starts.
        subprocess.check_call('chmod 666 /sys/module/i2c_bcm2708/parameters/combined', shell=True)
        subprocess.check_call('echo -n 1 > /sys/module/i2c_bcm2708/parameters/combined', shell=True)