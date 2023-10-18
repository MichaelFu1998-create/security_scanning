def forms_valid(self, form, inlines):
        """
        If the form and formsets are valid, save the associated models.
        """
        response = self.form_valid(form)
        for formset in inlines:
            formset.save()
        return response