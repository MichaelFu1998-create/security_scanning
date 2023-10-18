def settings_and_attributes(self):
        """Return a combined dictionary of setting values and attribute values."""
        attrs = self.setting_values()
        attrs.update(self.__dict__)
        skip = ["_instance_settings", "aliases"]
        for a in skip:
            del attrs[a]
        return attrs