def centralManagerDidUpdateState_(self, manager):
        """Called when the BLE adapter is powered on and ready to scan/connect
        to devices.
        """
        logger.debug('centralManagerDidUpdateState called')
        # Notify adapter about changed central state.
        get_provider()._adapter._state_changed(manager.state())