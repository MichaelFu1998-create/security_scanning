def use_winlegacy():
    """
    Forces use of the legacy Windows CryptoAPI. This should only be used on
    Windows XP or for testing. It is less full-featured than the Cryptography
    Next Generation (CNG) API, and as a result the elliptic curve and PSS
    padding features are implemented in pure Python. This isn't ideal, but it
    a shim for end-user client code. No one is going to run a server on Windows
    XP anyway, right?!

    :raises:
        EnvironmentError - when this function is called on an operating system other than Windows
        RuntimeError - when this function is called after another part of oscrypto has been imported
    """

    if sys.platform != 'win32':
        plat = platform.system() or sys.platform
        if plat == 'Darwin':
            plat = 'OS X'
        raise EnvironmentError('The winlegacy backend can only be used on Windows, not %s' % plat)

    with _backend_lock:
        if _module_values['backend'] is not None:
            raise RuntimeError(
                'Another part of oscrypto has already been imported, unable to force use of Windows legacy CryptoAPI'
            )
        _module_values['backend'] = 'winlegacy'