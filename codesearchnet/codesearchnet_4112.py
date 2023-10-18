def from_resolver(cls, spec_resolver):
        """Creates a customized Draft4ExtendedValidator.

        :param spec_resolver: resolver for the spec
        :type resolver: :class:`jsonschema.RefResolver`
        """
        spec_validators = cls._get_spec_validators(spec_resolver)
        return validators.extend(Draft4Validator, spec_validators)