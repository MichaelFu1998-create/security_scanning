def render(self, template, **kwargs):
        """ Render a route template and adds information to this route.

        :param template: Template name.
        :type template: str
        :param kwargs: dictionary of named arguments used to be passed to the template
        :type kwargs: dict
        :return: Http Response with rendered template
        :rtype: flask.Response
        """

        kwargs["cache_key"] = "%s" % kwargs["url"].values()
        kwargs["lang"] = self.get_locale()
        kwargs["assets"] = self.assets
        kwargs["main_collections"] = self.main_collections(kwargs["lang"])
        kwargs["cache_active"] = self.cache is not None
        kwargs["cache_time"] = 0
        kwargs["cache_key"], kwargs["cache_key_i18n"] = self.make_cache_keys(request.endpoint, kwargs["url"])
        kwargs["template"] = template

        for plugin in self.__plugins_render_views__:
            kwargs.update(plugin.render(**kwargs))

        return render_template(kwargs["template"], **kwargs)