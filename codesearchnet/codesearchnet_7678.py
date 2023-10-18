def get_preferred_collection(self):
        """If self.preferred_collection contains a D-Bus path,
        the collection at that address is returned. Otherwise,
        the default collection is returned.
        """
        bus = secretstorage.dbus_init()
        try:
            if hasattr(self, 'preferred_collection'):
                collection = secretstorage.Collection(
                    bus, self.preferred_collection)
            else:
                collection = secretstorage.get_default_collection(bus)
        except exceptions.SecretStorageException as e:
            raise InitError("Failed to create the collection: %s." % e)
        if collection.is_locked():
            collection.unlock()
            if collection.is_locked():  # User dismissed the prompt
                raise KeyringLocked("Failed to unlock the collection!")
        return collection