def post(self, request, response):
        """Processes a `POST` request."""
        if self.slug is not None:
            # Don't know what to do an item access.
            raise http.exceptions.NotImplemented()

        # Ensure we're allowed to create a resource.
        self.assert_operations('create')

        # Deserialize and clean the incoming object.
        data = self._clean(None, self.request.read(deserialize=True))

        # Delegate to `create` to create the item.
        item = self.create(data)

        # Build the response object.
        self.response.status = http.client.CREATED
        self.make_response(item)