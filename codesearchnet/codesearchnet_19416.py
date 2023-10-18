def is_compatible(cls, value):
        """
        Returns ``True`` if this model should be used to store ``value``.

        Checks if ``value`` is an instance of ``value_type``. Override this
        method if you need more advanced behaviour. For example, to distinguish
        between single and multi-line text.
        """
        if not hasattr(cls, 'value_type'):
            raise NotImplementedError(
                'You must define a `value_type` attribute or override the '
                '`is_compatible()` method on `SettingValueModel` subclasses.')
        return isinstance(value, cls.value_type)