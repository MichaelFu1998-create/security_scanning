def _ref(self, resp, base_name=None):
        """
        Store a response schema and return a reference to it.

        :param schema:
            Swagger response definition.
        :param base_name:
            Name that should be used for the reference.

        :rtype: dict
        :returns: JSON pointer to the original response definition.
        """

        name = base_name or resp.get('title', '') or resp.get('name', '')

        pointer = self.json_pointer + name
        self.response_registry[name] = resp

        return {'$ref': pointer}