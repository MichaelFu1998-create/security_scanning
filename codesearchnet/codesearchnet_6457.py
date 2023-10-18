def advertised(self):
        """Return a list of UUIDs for services that are advertised by this
        device.
        """
        uuids = []
        # Get UUIDs property but wrap it in a try/except to catch if the property
        # doesn't exist as it is optional.
        try:
            uuids = self._props.Get(_INTERFACE, 'UUIDs')
        except dbus.exceptions.DBusException as ex:
            # Ignore error if device has no UUIDs property (i.e. might not be
            # a BLE device).
            if ex.get_dbus_name() != 'org.freedesktop.DBus.Error.InvalidArgs':
                raise ex
        return [uuid.UUID(str(x)) for x in uuids]