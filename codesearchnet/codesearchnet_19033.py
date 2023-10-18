def save_formset(self, request, form, formset, change):
        """
        For each photo set it's author to currently authenticated user.
        """
        instances = formset.save(commit=False)
        for instance in instances:
            if isinstance(instance, Photo):
                instance.author = request.user
            instance.save()