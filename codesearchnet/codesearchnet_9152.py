def get_formset_kwargs(self):
        """
        Returns the keyword arguments for instantiating the formset.
        """
        # Perform deprecation check
        if hasattr(self, 'save_as_new'):
            klass = type(self).__name__
            raise DeprecationWarning(
                'Setting `{0}.save_as_new` at the class level is now '
                'deprecated. Set `{0}.formset_kwargs` instead.'.format(klass)
            )
        kwargs = super(BaseInlineFormSetFactory, self).get_formset_kwargs()
        kwargs['instance'] = self.object
        return kwargs