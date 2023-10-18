def __load_driver(name):
    """Tries to load the driver named @arg name.

    A driver is considered valid if it has a ahioDriverInfo object. It should
    however implement all APIs described in `ahio.abstract_driver`, as they'll
    be needed to use the driver.

    @returns the driver package, or False if it failed.
    """
    global __count
    try:
        dname = os.path.basename(name).replace('.py', '')
        mod_name = 'ahio.drivers.%s%d' % (dname, __count)
        loader = importlib.machinery.SourceFileLoader(mod_name, name)
        driver = loader.load_module()
        __count += 1
        return driver if hasattr(driver, 'ahioDriverInfo') else False
    except Exception:
        return False