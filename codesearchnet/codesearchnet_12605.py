def register_operators(*operators):
    """
    Registers one or multiple operators in the test engine.
    """
    def validate(operator):
        if isoperator(operator):
            return True

        raise NotImplementedError('invalid operator: {}'.format(operator))

    def register(operator):
        # Register operator by DSL keywords
        for name in operator.operators:
            # Check valid operators
            if name in Engine.operators:
                raise ValueError('operator name "{}" from {} is already '
                                 'in use by other operator'.format(
                                    name,
                                    operator.__name__
                                 ))

            # Register operator by name
            Engine.operators[name] = operator

    # Validates and registers operators
    [register(operator) for operator in operators if validate(operator)]