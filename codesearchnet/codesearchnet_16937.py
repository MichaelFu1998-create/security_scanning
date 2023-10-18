def convert(self, schema_node, definition_handler):
        """
        Convert node schema into a parameter object.
        """

        converted = {
            'name': schema_node.name,
            'in': self._in,
            'required': schema_node.required
        }
        if schema_node.description:
            converted['description'] = schema_node.description

        if schema_node.default:
            converted['default'] = schema_node.default

        schema = definition_handler(schema_node)
        # Parameters shouldn't have a title
        schema.pop('title', None)
        converted.update(schema)

        if schema.get('type') == 'array':
            converted['items'] = {'type': schema['items']['type']}

        return converted