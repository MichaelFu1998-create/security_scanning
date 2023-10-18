def delete(self, request, response):
        """Processes a `DELETE` request."""
        if self.slug is None:
            # Mass-DELETE is not implemented.
            raise http.exceptions.NotImplemented()

        # Ensure we're allowed to destroy a resource.
        self.assert_operations('destroy')

        # Delegate to `destroy` to destroy the item.
        self.destroy()

        # Build the response object.
        self.response.status = http.client.NO_CONTENT
        self.make_response()