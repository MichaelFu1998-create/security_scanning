def create(self, spec_resolver):
        """Creates json documents validator from spec resolver.
        :param spec_resolver: reference resolver.

        :return: RefResolver for spec with cached remote $refs used during
            validation.
        :rtype: :class:`jsonschema.RefResolver`
        """
        validator_cls = self.spec_validator_factory.from_resolver(
            spec_resolver)

        return validator_cls(
            self.schema, resolver=self.schema_resolver)