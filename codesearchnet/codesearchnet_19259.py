def routes_simple(self):
        """Returns simple info about registered blueprints

        :return: Tuple containing endpoint, path and allowed methods for each route
        """

        routes = []

        for bundle in self._registered_bundles:
            bundle_path = bundle['path']
            for blueprint in bundle['blueprints']:
                bp_path = blueprint['path']
                for child in blueprint['routes']:
                    routes.append(
                        (
                            child['endpoint'],
                            bundle_path + bp_path + child['path'],
                            child['methods']
                        )
                    )

        return routes