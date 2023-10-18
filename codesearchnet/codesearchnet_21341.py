def create_blueprint(self):
        """ Create blueprint and register rules

        :return: Blueprint of the current nemo app
        :rtype: flask.Blueprint
        """
        self.register_plugins()

        self.blueprint = Blueprint(
            self.name,
            "nemo",
            url_prefix=self.prefix,
            template_folder=self.template_folder,
            static_folder=self.static_folder,
            static_url_path=self.static_url_path
        )

        for url, name, methods, instance in self._urls:
            self.blueprint.add_url_rule(
                url,
                view_func=self.view_maker(name, instance),
                endpoint=_plugin_endpoint_rename(name, instance),
                methods=methods
            )

        for url, name, methods, instance in self._semantic_url:
            self.blueprint.add_url_rule(
                url,
                view_func=self.view_maker(name, instance),
                endpoint=_plugin_endpoint_rename(name, instance)+"_semantic",
                methods=methods
            )

        self.register_assets()
        self.register_filters()

        # We extend the loading list by the instance value
        self.__templates_namespaces__.extend(self.__instance_templates__)
        # We generate a template loader
        for namespace, directory in self.__templates_namespaces__[::-1]:
            if namespace not in self.__template_loader__:
                self.__template_loader__[namespace] = []
            self.__template_loader__[namespace].append(
                jinja2.FileSystemLoader(op.abspath(directory))
            )
        self.blueprint.jinja_loader = jinja2.PrefixLoader(
            {namespace: jinja2.ChoiceLoader(paths) for namespace, paths in self.__template_loader__.items()},
            "::"
        )

        if self.cache is not None:
            for func, instance in self.cached:
                setattr(instance, func.__name__, self.cache.memoize()(func))

        return self.blueprint