def get_sanitizer(self):
        """
        Get the field sanitizer.

        The priority is the first defined in the following order:
        - A sanitizer provided to the widget.
        - Profile (field settings) specific sanitizer, if defined in settings.
        - Global sanitizer defined in settings.
        - Simple no-op sanitizer which just returns the provided value.

        """
        sanitizer = self.sanitizer

        if not sanitizer:
            default_sanitizer = settings.CONFIG.get(self.SANITIZER_KEY)
            field_settings = getattr(self, 'field_settings', None)
            if isinstance(field_settings, six.string_types):
                profiles = settings.CONFIG.get(self.SANITIZER_PROFILES_KEY, {})
                sanitizer = profiles.get(field_settings, default_sanitizer)
            else:
                sanitizer = default_sanitizer

        if isinstance(sanitizer, six.string_types):
            sanitizer = import_string(sanitizer)

        return sanitizer or noop