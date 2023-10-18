def get(self, q=None, page=None):
        """Get styles."""
        # Check cache to exit early if needed
        etag = generate_etag(current_ext.content_version.encode('utf8'))
        self.check_etag(etag, weak=True)

        # Build response
        res = jsonify(current_ext.styles)
        res.set_etag(etag)

        return res