def get(self, request, *args, **kwargs):
        """
        Handles GET requests and instantiates a blank version of the form and formsets.
        """
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        inlines = self.construct_inlines()
        return self.render_to_response(self.get_context_data(form=form, inlines=inlines, **kwargs))