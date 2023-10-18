def _ref_recursive(self, schema, depth, base_name=None):
        """
        Dismantle nested swagger schemas into several definitions using JSON pointers.
        Note: This can be dangerous since definition titles must be unique.

        :param schema:
            Base swagger schema.
        :param depth:
            How many levels of the swagger object schemas should be split into
            swaggger definitions with JSON pointers. Default (0) is no split.
            You may use negative values to split everything.
        :param base_name:
            If schema doesn't have a name, the caller may provide it to be
            used as reference.

        :rtype: dict
        :returns:
            JSON pointer to the root definition schema,
            or the original definition if depth is zero.
        """

        if depth == 0:
            return schema

        if schema['type'] != 'object':
            return schema

        name = base_name or schema['title']

        pointer = self.json_pointer + name
        for child_name, child in schema.get('properties', {}).items():
            schema['properties'][child_name] = self._ref_recursive(child, depth-1)

        self.definition_registry[name] = schema

        return {'$ref': pointer}