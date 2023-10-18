def find_device(self, service_uuids=[], name=None, timeout_sec=TIMEOUT_SEC):
        """Return the first device that advertises the specified service UUIDs or
        has the specified name. Will wait up to timeout_sec seconds for the device
        to be found, and if the timeout is zero then it will not wait at all and
        immediately return a result.  When no device is found a value of None is
        returned.
        """
        start = time.time()
        while True:
            # Call find_devices and grab the first result if any are found.
            found = self.find_devices(service_uuids, name)
            if len(found) > 0:
                return found[0]
            # No device was found.  Check if the timeout is exceeded and wait to
            # try again.
            if time.time()-start >= timeout_sec:
                # Failed to find a device within the timeout.
                return None
            time.sleep(1)