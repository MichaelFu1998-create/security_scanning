def enable_FTDI_driver():
    """Re-enable the FTDI drivers for the current platform."""
    logger.debug('Enabling FTDI driver.')
    if sys.platform == 'darwin':
        logger.debug('Detected Mac OSX')
        # Mac OS commands to enable FTDI driver.
        _check_running_as_root()
        subprocess.check_call('kextload -b com.apple.driver.AppleUSBFTDI', shell=True)
        subprocess.check_call('kextload /System/Library/Extensions/FTDIUSBSerialDriver.kext', shell=True)
    elif sys.platform.startswith('linux'):
        logger.debug('Detected Linux')
        # Linux commands to enable FTDI driver.
        _check_running_as_root()
        subprocess.check_call('modprobe -q ftdi_sio', shell=True)
        subprocess.check_call('modprobe -q usbserial', shell=True)