def construct_formset(self):
        """
        Returns an instance of the formset
        """
        formset_class = self.get_formset()
        if hasattr(self, 'get_extra_form_kwargs'):
            klass = type(self).__name__
            raise DeprecationWarning(
                'Calling {0}.get_extra_form_kwargs is no longer supported. '
                'Set `form_kwargs` in {0}.formset_kwargs or override '
                '{0}.get_formset_kwargs() directly.'.format(klass),
            )
        return formset_class(**self.get_formset_kwargs())