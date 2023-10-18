def get_formset_kwargs(self):
        """
        Returns the keyword arguments for instantiating the formset.
        """
        kwargs = self.formset_kwargs.copy()
        kwargs.update({
            'initial': self.get_initial(),
            'prefix': self.get_prefix(),
        })

        if self.request.method in ('POST', 'PUT'):
            kwargs.update({
                'data': self.request.POST.copy(),
                'files': self.request.FILES,
            })
        return kwargs