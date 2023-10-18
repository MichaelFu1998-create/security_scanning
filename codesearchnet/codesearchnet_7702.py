def get_attached_devices_2(self):
        """
        Return list of connected devices to the router with details.

        This call is slower and probably heavier on the router load.

        Returns None if error occurred.
        """
        _LOGGER.info("Get attached devices 2")

        success, response = self._make_request(SERVICE_DEVICE_INFO,
                                               "GetAttachDevice2")
        if not success:
            return None

        success, devices_node = _find_node(
            response.text,
            ".//GetAttachDevice2Response/NewAttachDevice")
        if not success:
            return None

        xml_devices = devices_node.findall("Device")
        devices = []
        for d in xml_devices:
            ip = _xml_get(d, 'IP')
            name = _xml_get(d, 'Name')
            mac = _xml_get(d, 'MAC')
            signal = _convert(_xml_get(d, 'SignalStrength'), int)
            link_type = _xml_get(d, 'ConnectionType')
            link_rate = _xml_get(d, 'Linkspeed')
            allow_or_block = _xml_get(d, 'AllowOrBlock')
            device_type = _convert(_xml_get(d, 'DeviceType'), int)
            device_model = _xml_get(d, 'DeviceModel')
            ssid = _xml_get(d, 'SSID')
            conn_ap_mac = _xml_get(d, 'ConnAPMAC')
            devices.append(Device(name, ip, mac, link_type, signal, link_rate,
                                  allow_or_block, device_type, device_model,
                                  ssid, conn_ap_mac))

        return devices