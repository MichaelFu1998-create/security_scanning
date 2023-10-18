def attach_bp(self, bp, description=''):
        """Attaches a flask.Blueprint to the bundle

        :param bp: :class:`flask.Blueprint` object
        :param description: Optional description string
        :raises:
            - InvalidBlueprint if the Blueprint is not of type `flask.Blueprint`
        """

        if not isinstance(bp, Blueprint):
            raise InvalidBlueprint('Blueprints attached to the bundle must be of type {0}'.format(Blueprint))

        self.blueprints.append((bp, description))