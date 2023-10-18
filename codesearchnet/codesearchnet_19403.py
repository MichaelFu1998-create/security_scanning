def get_value(self, context, default):
        """
        Returns a ``SettingDict`` object.
        """
        if default is None:
            settings = self.setting_model.objects.as_dict()
        else:
            settings = self.setting_model.objects.as_dict(default=default)
        return settings