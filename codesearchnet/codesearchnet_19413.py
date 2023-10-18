def as_dict(self, default=None):
        """
        Returns a ``SettingDict`` object for this queryset.
        """
        settings = SettingDict(queryset=self, default=default)
        return settings