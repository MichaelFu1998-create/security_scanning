def get_content(self):
        """Open content as a stream for reading.

        See DAVResource.get_content()
        """
        assert not self.is_collection
        d = self.fctx.data()
        return compat.StringIO(d)