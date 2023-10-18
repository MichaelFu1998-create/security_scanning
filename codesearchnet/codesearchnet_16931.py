def generate(self, title=None, version=None, base_path=None,
                 info=None, swagger=None, **kwargs):
        """Generate a Swagger 2.0 documentation. Keyword arguments may be used
        to provide additional information to build methods as such ignores.

        :param title:
            The name presented on the swagger document.
        :param version:
            The version of the API presented on the swagger document.
        :param base_path:
            The path that all requests to the API must refer to.
        :param info:
            Swagger info field.
        :param swagger:
            Extra fields that should be provided on the swagger documentation.

        :rtype: dict
        :returns: Full OpenAPI/Swagger compliant specification for the application.
        """
        title = title or self.api_title
        version = version or self.api_version
        info = info or self.swagger.get('info', {})
        swagger = swagger or self.swagger
        base_path = base_path or self.base_path

        swagger = swagger.copy()
        info.update(title=title, version=version)
        swagger.update(swagger='2.0', info=info, basePath=base_path)

        paths, tags = self._build_paths()

        # Update the provided tags with the extracted ones preserving order
        if tags:
            swagger.setdefault('tags', [])
            tag_names = {t['name'] for t in swagger['tags']}
            for tag in tags:
                if tag['name'] not in tag_names:
                    swagger['tags'].append(tag)

        # Create/Update swagger sections with extracted values where not provided
        if paths:
            swagger.setdefault('paths', {})
            merge_dicts(swagger['paths'], paths)

        definitions = self.definitions.definition_registry
        if definitions:
            swagger.setdefault('definitions', {})
            merge_dicts(swagger['definitions'], definitions)

        parameters = self.parameters.parameter_registry
        if parameters:
            swagger.setdefault('parameters', {})
            merge_dicts(swagger['parameters'], parameters)

        responses = self.responses.response_registry
        if responses:
            swagger.setdefault('responses', {})
            merge_dicts(swagger['responses'], responses)

        return swagger