def _register_blueprint(self, app, bp, bundle_path, child_path, description):
        """Register and return info about the registered blueprint

        :param bp: :class:`flask.Blueprint` object
        :param bundle_path: the URL prefix of the bundle
        :param child_path: blueprint relative to the bundle path
        :return: Dict with info about the blueprint
        """

        base_path = sanitize_path(self._journey_path + bundle_path + child_path)

        app.register_blueprint(bp, url_prefix=base_path)

        return {
            'name': bp.name,
            'path': child_path,
            'import_name': bp.import_name,
            'description': description,
            'routes': self.get_blueprint_routes(app, base_path)
        }