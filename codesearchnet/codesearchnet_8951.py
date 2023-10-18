def type_cast(self, item, schema=None):
        """
        Loops over item and performs type casting
        according to supplied schema fragment
        """
        if schema is None:
            schema = self._schema
        properties = schema['properties']
        for key, value in item.items():
            if key not in properties:
                continue
            try:
                json_type = properties[key]['type']
            except KeyError:
                json_type = None
            if json_type == 'integer' and not isinstance(value, int):
                value = int(value)
            elif json_type == 'boolean' and not isinstance(value, bool):
                value = value == '1'
            item[key] = value
        return item