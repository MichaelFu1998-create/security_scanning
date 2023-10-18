def allow_block_device(self, mac_addr, device_status=BLOCK):
        """
        Allow or Block a device via its Mac Address.
        Pass in the mac address for the device that you want to set. Pass in the
        device_status you wish to set the device to: Allow (allow device to access the
        network) or Block (block the device from accessing the network).
        """
        _LOGGER.info("Allow block device")
        if self.config_started:
            _LOGGER.error("Inconsistant configuration state, configuration already started")
            return False

        if not self.config_start():
            _LOGGER.error("Could not start configuration")
            return False

        success, _ = self._make_request(
            SERVICE_DEVICE_CONFIG, "SetBlockDeviceByMAC",
            {"NewAllowOrBlock": device_status, "NewMACAddress": mac_addr})

        if not success:
            _LOGGER.error("Could not successfully call allow/block device")
            return False

        if not self.config_finish():
            _LOGGER.error("Inconsistant configuration state, configuration already finished")
            return False

        return True