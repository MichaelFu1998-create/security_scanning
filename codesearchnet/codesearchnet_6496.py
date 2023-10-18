def get_provider():
    """Return an instance of the BLE provider for the current platform."""
    global _provider
    # Set the provider based on the current platform.
    if _provider is None:
        if sys.platform.startswith('linux'):
            # Linux platform
            from .bluez_dbus.provider import BluezProvider
            _provider = BluezProvider()
        elif sys.platform == 'darwin':
            # Mac OSX platform
            from .corebluetooth.provider import CoreBluetoothProvider
            _provider = CoreBluetoothProvider()
        else:
            # Unsupported platform
            raise RuntimeError('Sorry the {0} platform is not supported by the BLE library!'.format(sys.platform))
    return _provider