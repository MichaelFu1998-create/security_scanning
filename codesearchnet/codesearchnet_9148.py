def get_factory_kwargs(self):
        """
        Returns the keyword arguments for calling the formset factory
        """
        # Perform deprecation check
        for attr in ['extra', 'max_num', 'can_order', 'can_delete', 'ct_field',
                     'formfield_callback', 'fk_name', 'widgets', 'ct_fk_field']:
            if hasattr(self, attr):
                klass = type(self).__name__
                raise DeprecationWarning(
                    'Setting `{0}.{1}` at the class level is now deprecated. '
                    'Set `{0}.factory_kwargs` instead.'.format(klass, attr)
                )

        kwargs = self.factory_kwargs.copy()
        if self.get_formset_class():
            kwargs['formset'] = self.get_formset_class()
        return kwargs