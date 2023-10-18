def _extract_transform_colander_schema(self, args):
        """
        Extract schema from view args and transform it using
        the pipeline of schema transformers

        :param args:
            Arguments from the view decorator.

        :rtype: colander.MappingSchema()
        :returns: View schema cloned and transformed
        """

        schema = args.get('schema', colander.MappingSchema())
        if not isinstance(schema, colander.Schema):
            schema = schema()
        schema = schema.clone()
        for transformer in self.schema_transformers:
            schema = transformer(schema, args)
        return schema