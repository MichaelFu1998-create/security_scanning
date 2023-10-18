def get_value(self, context, name, default):
        """
        Returns the value of the named setting.
        """
        settings = self.setting_model.objects.filter(name=name)
        if default is None:
            settings = settings.as_dict()
        else:
            settings = settings.as_dict(default=default)
        value = settings[name]
        return value