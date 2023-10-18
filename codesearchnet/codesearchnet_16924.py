def from_schema(self, schema_node, base_name=None):
        """
        Creates a Swagger definition from a colander schema.

        :param schema_node:
            Colander schema to be transformed into a Swagger definition.
        :param base_name:
            Schema alternative title.

        :rtype: dict
        :returns: Swagger schema.
        """
        return self._ref_recursive(self.type_converter(schema_node), self.ref, base_name)