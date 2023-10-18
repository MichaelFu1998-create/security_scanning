def view_maker(self, name, instance=None):
        """ Create a view

        :param name: Name of the route function to use for the view.
        :type name: str
        :return: Route function which makes use of Nemo context (such as menu informations)
        :rtype: function
        """
        if instance is None:
            instance = self
        sig = "lang" in [
            parameter.name
            for parameter in inspect.signature(getattr(instance, name)).parameters.values()
        ]

        def route(**kwargs):
            if sig and "lang" not in kwargs:
                kwargs["lang"] = self.get_locale()
            if "semantic" in kwargs:
                del kwargs["semantic"]
            return self.route(getattr(instance, name), **kwargs)
        return route