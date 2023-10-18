def put(self, request, response):
        """Processes a `PUT` request."""
        if self.slug is None:
            # Mass-PUT is not implemented.
            raise http.exceptions.NotImplemented()

        # Check if the resource exists.
        target = self.read()

        # Deserialize and clean the incoming object.
        data = self._clean(target, self.request.read(deserialize=True))

        if target is not None:
            # Ensure we're allowed to update the resource.
            self.assert_operations('update')

            try:
                # Delegate to `update` to create the item.
                self.update(target, data)

            except AttributeError:
                # No read method defined.
                raise http.exceptions.NotImplemented()

            # Build the response object.
            self.make_response(target)

        else:
            # Ensure we're allowed to create the resource.
            self.assert_operations('create')

            # Delegate to `create` to create the item.
            target = self.create(data)

            # Build the response object.
            self.response.status = http.client.CREATED
            self.make_response(target)