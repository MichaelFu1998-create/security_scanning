def find_device(cls, timeout_sec=TIMEOUT_SEC):
        """Find the first available device that supports this service and return
        it, or None if no device is found.  Will wait for up to timeout_sec
        seconds to find the device.
        """
        return get_provider().find_device(service_uuids=cls.ADVERTISED, timeout_sec=timeout_sec)