def strip_fixed_params(payload):
        """strip(12 byte) wlan_mgt.fixed.all
        :payload: ctypes.structure
        :return: int
            timestamp
        :return: int
            beacon interval
        :return: dict
            capabilities
        """
        if len(payload) != 12:
            return None, None, None
        idx = 0
        timestamp = Management.get_timestamp(payload[idx:idx + 8])
        idx += 8
        interval = Management.get_interval(payload[idx:idx + 2])
        idx += 2
        capabils = Management.get_fixed_capabils(payload[idx:idx + 2])
        return timestamp, interval, capabils