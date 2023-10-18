def get_field_settings(self):
        """
        Get the field settings, if the configured setting is a string try
        to get a 'profile' from the global config.
        """
        field_settings = None
        if self.field_settings:
            if isinstance(self.field_settings, six.string_types):
                profiles = settings.CONFIG.get(self.PROFILE_KEY, {})
                field_settings = profiles.get(self.field_settings)
            else:
                field_settings = self.field_settings
        return field_settings