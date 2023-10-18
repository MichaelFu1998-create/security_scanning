def get(self, request, response):
        """Processes a `GET` request."""
        # Ensure we're allowed to read the resource.
        self.assert_operations('read')

        # Delegate to `read` to retrieve the items.
        items = self.read()

        # if self.slug is not None and not items:
        #     # Requested a specific resource but nothing is returned.

        #     # Attempt to resolve by changing what we understand as
        #     # a slug to a path.
        #     self.path = self.path + self.slug if self.path else self.slug
        #     self.slug = None

        #     # Attempt to retreive the resource again.
        #     items = self.read()

        # Ensure that if we have a slug and still no items that a 404
        # is rasied appropriately.
        if not items:
            raise http.exceptions.NotFound()

        if (isinstance(items, Iterable)
                and not isinstance(items, six.string_types)) and items:
            # Paginate over the collection.
            items = pagination.paginate(self.request, self.response, items)

        # Build the response object.
        self.make_response(items)