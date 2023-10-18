def param_changed_to(self, key, to_value, from_value=None):
        """
        Returns true if the given parameter, with name key, has transitioned to the given value.
        """
        last_value = getattr(self.last_manifest, key)
        current_value = self.current_manifest.get(key)
        if from_value is not None:
            return last_value == from_value and current_value == to_value
        return last_value != to_value and current_value == to_value