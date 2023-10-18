def get_factory_kwargs(self):
        """
        Returns the keyword arguments for calling the formset factory
        """
        kwargs = super(BaseInlineFormSetFactory, self).get_factory_kwargs()
        kwargs.setdefault('fields', self.fields)
        kwargs.setdefault('exclude', self.exclude)

        if self.get_form_class():
            kwargs['form'] = self.get_form_class()
        return kwargs