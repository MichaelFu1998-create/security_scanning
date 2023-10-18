def handle_int(self, item):
        """Helper method for fetching a integer value."""
        doc = yield from self.handle_get(item)
        if doc is None:
            return None

        return int(doc.value.u8.text) or None