def get_model_for_value(cls, value):
        """
        Iterates through setting value subclasses, returning one that is
        compatible with the type of ``value``. Calls ``is_compatible()`` on
        each subclass.
        """
        for related_object in get_all_related_objects(cls._meta):
            model = getattr(related_object, 'related_model', related_object.model)
            if issubclass(model, cls):
                if model.is_compatible(value):
                    return model
        raise ValueError(
            'No compatible `SettingValueModel` subclass for %r' % value)