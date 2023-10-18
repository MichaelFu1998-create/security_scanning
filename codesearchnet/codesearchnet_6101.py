def set_share_path(self, share_path):
        """Set application location for this resource provider.

        @param share_path: a UTF-8 encoded, unquoted byte string.
        """
        # if isinstance(share_path, unicode):
        #     share_path = share_path.encode("utf8")
        assert share_path == "" or share_path.startswith("/")
        if share_path == "/":
            share_path = ""  # This allows to code 'absPath = share_path + path'
        assert share_path in ("", "/") or not share_path.endswith("/")
        self.share_path = share_path