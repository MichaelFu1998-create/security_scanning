def handle_long(self, item):
        """Helper method for fetching a long value. Result is integer."""
        doc = yield from self.handle_get(item)
        if doc is None:
            return None

        return int(doc.value.u32.text) or None