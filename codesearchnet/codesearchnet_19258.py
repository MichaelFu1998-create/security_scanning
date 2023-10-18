def init_app(self, app):
        """Initializes Journey extension

        :param app: App passed from constructor or directly to init_app
        :raises:
            - NoBundlesAttached if no bundles has been attached attached

        """

        if len(self._attached_bundles) == 0:
            raise NoBundlesAttached("At least one bundle must be attached before initializing Journey")

        for bundle in self._attached_bundles:
            processed_bundle = {
                'path': bundle.path,
                'description': bundle.description,
                'blueprints': []
            }

            for (bp, description) in bundle.blueprints:
                # Register the BP
                blueprint = self._register_blueprint(app, bp, bundle.path,
                                                     self.get_bp_path(bp), description)

                # Finally, attach the blueprints to its parent
                processed_bundle['blueprints'].append(blueprint)

            self._registered_bundles.append(processed_bundle)