def traverse(cls, request, params=None):
        """Traverses down the path and determines the accessed resource.

        This makes use of the patterns array to implement simple traversal.
        This defaults to a no-op if there are no defined patterns.
        """
        # Attempt to parse the path using a pattern.
        result = cls.parse(request.path)
        if result is None:
            # No parsing was requested; no-op.
            return cls, {}

        elif not result:
            # Parsing failed; raise 404.
            raise http.exceptions.NotFound()

        # Partition out the result.
        resource, data, rest = result

        if params:
            # Append params to data.
            data.update(params)

        if resource is None:
            # No traversal; return parameters.
            return cls, data

        # Modify the path appropriately.
        if data.get('path') is not None:
            request.path = data.pop('path')

        elif rest is not None:
            request.path = rest

        # Send us through traversal again.
        result = resource.traverse(request, params=data)
        return result