def register_simple_chooser(self, model, **kwargs):
        """
        Generates a model chooser definition from a model, and adds it to the
        registry.
        """
        name = '{}Chooser'.format(model._meta.object_name)
        attrs = {'model': model}
        attrs.update(kwargs)

        chooser = type(name, (Chooser,), attrs)
        self.register_chooser(chooser)

        return model