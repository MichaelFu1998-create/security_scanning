def create(self, name, value):
        """
        Creates and returns an object of the appropriate type for ``value``.
        """
        if value is None:
            raise ValueError('Setting value cannot be `None`.')
        model = Setting.get_model_for_value(value)
        # Call `create()` method on the super class to avoid recursion.
        obj = super(SettingQuerySet, model.objects.all()) \
            .create(name=name, value=value)
        return obj