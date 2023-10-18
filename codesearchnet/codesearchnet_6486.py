def _get_objects(self, interface, parent_path='/org/bluez'):
        """Return a list of all bluez DBus objects that implement the requested
        interface name and are under the specified path.  The default is to
        search devices under the root of all bluez objects.
        """
        # Iterate through all the objects in bluez's DBus hierarchy and return
        # any that implement the requested interface under the specified path.
        parent_path = parent_path.lower()
        objects = []
        for opath, interfaces in iteritems(self._bluez.GetManagedObjects()):
            if interface in interfaces.keys() and opath.lower().startswith(parent_path):
                objects.append(self._bus.get_object('org.bluez', opath))
        return objects