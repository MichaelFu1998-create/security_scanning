def from_schema_mapping(self, schema_mapping):
        """
        Creates a Swagger response object from a dict of response schemas.

        :param schema_mapping:
            Dict with entries matching ``{status_code: response_schema}``.
        :rtype: dict
        :returns: Response schema.
        """

        responses = {}

        for status, response_schema in schema_mapping.items():

            response = {}
            if response_schema.description:
                response['description'] = response_schema.description
            else:
                raise CorniceSwaggerException('Responses must have a description.')

            for field_schema in response_schema.children:
                location = field_schema.name

                if location == 'body':
                    title = field_schema.__class__.__name__
                    if title == 'body':
                        title = response_schema.__class__.__name__ + 'Body'
                    field_schema.title = title
                    response['schema'] = self.definitions.from_schema(field_schema)

                elif location in ('header', 'headers'):
                    header_schema = self.type_converter(field_schema)
                    headers = header_schema.get('properties')
                    if headers:
                        # Response headers doesn't accept titles
                        for header in headers.values():
                            header.pop('title')

                        response['headers'] = headers

            pointer = response_schema.__class__.__name__
            if self.ref:
                response = self._ref(response, pointer)
            responses[status] = response

        return responses