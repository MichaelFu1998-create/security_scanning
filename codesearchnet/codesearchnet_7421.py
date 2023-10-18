def item_fields(self):
        """ Get all available item fields
        """
        # Check for a valid cached version
        if self.templates.get("item_fields") and not self._updated(
            "/itemFields", self.templates["item_fields"], "item_fields"
        ):
            return self.templates["item_fields"]["tmplt"]
        query_string = "/itemFields"
        # otherwise perform a normal request and cache the response
        retrieved = self._retrieve_data(query_string)
        return self._cache(retrieved, "item_fields")