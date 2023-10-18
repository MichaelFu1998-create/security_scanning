def _get_objects_by_path(self, paths):
        """Return a list of all bluez DBus objects from the provided list of paths.
        """
        return map(lambda x: self._bus.get_object('org.bluez', x), paths)