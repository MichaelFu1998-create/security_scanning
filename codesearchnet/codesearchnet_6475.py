def peripheral_didReadRSSI_error_(self, peripheral, rssi, error):
        """Called when a new RSSI value for the peripheral is available."""
        logger.debug('peripheral_didReadRSSI_error called')
        # Note this appears to be completely undocumented at the time of this
        # writing.  Can see more details at:
        #  http://stackoverflow.com/questions/25952218/ios-8-corebluetooth-deprecated-rssi-methods
        # Stop if there was some kind of error.
        if error is not None:
            return
        # Notify the device about the updated RSSI value.
        device = device_list().get(peripheral)
        if device is not None:
            device._rssi_changed(rssi)