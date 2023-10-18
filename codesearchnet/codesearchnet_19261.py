def attach_bundle(self, bundle):
        """Attaches a bundle object

        :param bundle: :class:`flask_journey.BlueprintBundle` object
        :raises:
            - IncompatibleBundle if the bundle is not of type `BlueprintBundle`
            - ConflictingPath if a bundle already exists at bundle.path
            - MissingBlueprints if the bundle doesn't contain any blueprints
        """

        if not isinstance(bundle, BlueprintBundle):
            raise IncompatibleBundle('BlueprintBundle object passed to attach_bundle must be of type {0}'
                                     .format(BlueprintBundle))
        elif len(bundle.blueprints) == 0:
            raise MissingBlueprints("Bundles must contain at least one flask.Blueprint")
        elif self._bundle_exists(bundle.path):
            raise ConflictingPath("Duplicate bundle path {0}".format(bundle.path))
        elif self._journey_path == bundle.path == '/':
            raise ConflictingPath("Bundle path and Journey path cannot both be {0}".format(bundle.path))

        self._attached_bundles.append(bundle)