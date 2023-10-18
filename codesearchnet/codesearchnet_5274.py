def disable_FTDI_driver():
    """Disable the FTDI drivers for the current platform.  This is necessary
    because they will conflict with libftdi and accessing the FT232H.  Note you
    can enable the FTDI drivers again by calling enable_FTDI_driver.
    """
    logger.debug('Disabling FTDI driver.')
    if sys.platform == 'darwin':
        logger.debug('Detected Mac OSX')
        # Mac OS commands to disable FTDI driver.
        _check_running_as_root()
        subprocess.call('kextunload -b com.apple.driver.AppleUSBFTDI', shell=True)
        subprocess.call('kextunload /System/Library/Extensions/FTDIUSBSerialDriver.kext', shell=True)
    elif sys.platform.startswith('linux'):
        logger.debug('Detected Linux')
        # Linux commands to disable FTDI driver.
        _check_running_as_root()
        subprocess.call('modprobe -r -q ftdi_sio', shell=True)
        subprocess.call('modprobe -r -q usbserial', shell=True)