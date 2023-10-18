def get_context_data(self, **kwargs):
        """
        If `inlines_names` has been defined, add each formset to the context under
        its corresponding entry in `inlines_names`
        """
        context = {}
        inlines_names = self.get_inlines_names()

        if inlines_names:
            # We have formset or inlines in context, but never both
            context.update(zip(inlines_names, kwargs.get('inlines', [])))
            if 'formset' in kwargs:
                context[inlines_names[0]] = kwargs['formset']
        context.update(kwargs)
        return super(NamedFormsetsMixin, self).get_context_data(**context)