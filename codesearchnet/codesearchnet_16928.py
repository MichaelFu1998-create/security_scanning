def _ref(self, param, base_name=None):
        """
        Store a parameter schema and return a reference to it.

        :param schema:
            Swagger parameter definition.
        :param base_name:
            Name that should be used for the reference.

        :rtype: dict
        :returns: JSON pointer to the original parameter definition.
        """

        name = base_name or param.get('title', '') or param.get('name', '')

        pointer = self.json_pointer + name
        self.parameter_registry[name] = param

        return {'$ref': pointer}