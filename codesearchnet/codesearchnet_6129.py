def _find(self, url):
        """Return properties document for path."""
        # Query the permanent view to find a url
        vr = self.db.view("properties/by_url", key=url, include_docs=True)
        _logger.debug("find(%r) returned %s" % (url, len(vr)))
        assert len(vr) <= 1, "Found multiple matches for %r" % url
        for row in vr:
            assert row.doc
            return row.doc
        return None