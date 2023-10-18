def from_schema(self, schema_node):
        """
        Creates a list of Swagger params from a colander request schema.

        :param schema_node:
            Request schema to be transformed into Swagger.
        :param validators:
            Validators used in colander with the schema.

        :rtype: list
        :returns: List of Swagger parameters.
        """

        params = []

        for param_schema in schema_node.children:
            location = param_schema.name
            if location is 'body':
                name = param_schema.__class__.__name__
                if name == 'body':
                    name = schema_node.__class__.__name__ + 'Body'
                param = self.parameter_converter(location,
                                                 param_schema)
                param['name'] = name
                if self.ref:
                    param = self._ref(param)
                params.append(param)

            elif location in (('path', 'header', 'headers', 'querystring', 'GET')):
                for node_schema in param_schema.children:
                    param = self.parameter_converter(location, node_schema)
                    if self.ref:
                        param = self._ref(param)
                    params.append(param)

        return params