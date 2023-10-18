def construct_inlines(self):
        """
        Returns the inline formset instances
        """
        inline_formsets = []
        for inline_class in self.get_inlines():
            inline_instance = inline_class(self.model, self.request, self.object, self.kwargs, self)
            inline_formset = inline_instance.construct_formset()
            inline_formsets.append(inline_formset)
        return inline_formsets