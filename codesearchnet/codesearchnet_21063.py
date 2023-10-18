def handle_set(self, item, value):
        """Helper method for setting a value by using the fsapi API."""
        doc = yield from self.call('SET/{}'.format(item), dict(value=value))
        if doc is None:
            return None

        return doc.status == 'FS_OK'