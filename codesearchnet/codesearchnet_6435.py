def _update_advertised(self, advertised):
        """Called when advertisement data is received."""
        # Advertisement data was received, pull out advertised service UUIDs and
        # name from advertisement data.
        if 'kCBAdvDataServiceUUIDs' in advertised:
            self._advertised = self._advertised + map(cbuuid_to_uuid, advertised['kCBAdvDataServiceUUIDs'])