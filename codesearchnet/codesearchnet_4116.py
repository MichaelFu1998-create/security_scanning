def from_spec_resolver(cls, spec_resolver):
        """Creates validators generator for the spec resolver.

        :param spec_resolver: resolver for the spec
        :type instance_resolver: :class:`jsonschema.RefResolver`
        """
        deref = DerefValidatorDecorator(spec_resolver)
        for key, validator_callable in iteritems(cls.validators):
            yield key, deref(validator_callable)