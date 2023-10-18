def discover(cls, device, timeout_sec=TIMEOUT_SEC):
        """Wait until the specified device has discovered the expected services
        and characteristics for this service.  Should be called once before other
        calls are made on the service.  Returns true if the service has been
        discovered in the specified timeout, or false if not discovered.
        """
        device.discover(cls.SERVICES, cls.CHARACTERISTICS, timeout_sec)