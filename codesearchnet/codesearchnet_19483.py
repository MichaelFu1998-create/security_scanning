def get_child_models(self):
        """
        Returns a list of ``(Model, ModelAdmin)`` tuples for ``base_model``
        subclasses.
        """
        child_models = []
        # Loop through all models with FKs back to `base_model`.
        for related_object in get_all_related_objects(self.base_model._meta):
            # Django 1.8 deprecated `get_all_related_objects()`. We're still
            # using it for now with the documented work-around for
            # compatibility with Django <=1.7.
            model = getattr(
                related_object, 'related_model', related_object.model)
            # Only consider `base_model` subclasses.
            if issubclass(model, self.base_model):
                class SettingValueAdmin(self.base_admin_class):
                    pass
                child_models.append((model, SettingValueAdmin))
        return child_models