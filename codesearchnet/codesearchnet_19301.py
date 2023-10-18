def refresh(self):
        """
        Updates the cache with setting values from the database.
        """
        # `values_list('name', 'value')` doesn't work because `value` is not a
        # setting (base class) field, it's a setting value (subclass) field. So
        # we have to get real instances.
        args = [(obj.name, obj.value) for obj in self.queryset.all()]
        super(SettingDict, self).update(args)
        self.empty_cache = False