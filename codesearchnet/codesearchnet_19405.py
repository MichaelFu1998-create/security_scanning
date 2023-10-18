def render_tag(self, context, name, nodelist):
        """
        Returns the value of the named setting.
        """
        # Use `try` and `except` instead of `setdefault()` so we can skip
        # rendering the nodelist when the setting already exists.
        settings = self.setting_model.objects.filter(name=name).as_dict()
        try:
            value = settings[name]
        except KeyError:
            value = settings[name] = nodelist.render(context)
        return value