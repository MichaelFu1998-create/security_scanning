def register(self):
        """ Register the app using Blueprint

        :return: Nemo blueprint
        :rtype: flask.Blueprint
        """
        if self.app is not None:
            if not self.blueprint:
                self.blueprint = self.create_blueprint()
            self.app.register_blueprint(self.blueprint)
            if self.cache is None:
                # We register a fake cache extension.
                setattr(self.app.jinja_env, "_fake_cache_extension", self)
                self.app.jinja_env.add_extension(FakeCacheExtension)
            return self.blueprint
        return None