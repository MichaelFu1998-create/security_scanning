def peripheral_didDiscoverServices_(self, peripheral, services):
        """Called when services are discovered for a device."""
        logger.debug('peripheral_didDiscoverServices called')
        # Make sure the discovered services are added to the list of known
        # services, and kick off characteristic discovery for each one.
        # NOTE: For some reason the services parameter is never set to a good
        # value, instead you must query peripheral.services() to enumerate the
        # discovered services.
        for service in peripheral.services():
            if service_list().get(service) is None:
                service_list().add(service, CoreBluetoothGattService(service))
            # Kick off characteristic discovery for this service.  Just discover
            # all characteristics for now.
            peripheral.discoverCharacteristics_forService_(None, service)