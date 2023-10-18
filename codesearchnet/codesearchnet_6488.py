def _print_tree(self):
        """Print tree of all bluez objects, useful for debugging."""
        # This is based on the bluez sample code get-managed-objects.py.
        objects = self._bluez.GetManagedObjects()
        for path in objects.keys():
            print("[ %s ]" % (path))
            interfaces = objects[path]
            for interface in interfaces.keys():
                if interface in ["org.freedesktop.DBus.Introspectable",
                            "org.freedesktop.DBus.Properties"]:
                    continue
                print("    %s" % (interface))
                properties = interfaces[interface]
                for key in properties.keys():
                    print("      %s = %s" % (key, properties[key]))