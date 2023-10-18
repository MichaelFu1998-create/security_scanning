def handle_text(self, item):
        """Helper method for fetching a text value."""
        doc = yield from self.handle_get(item)
        if doc is None:
            return None

        return doc.value.c8_array.text or None