def construct_formset(self):
        """
        Overrides construct_formset to attach the model class as
        an attribute of the returned formset instance.
        """
        formset = super(InlineFormSetFactory, self).construct_formset()
        formset.model = self.inline_model
        return formset