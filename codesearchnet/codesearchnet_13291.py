def handle_authorized_event(self, event):
        """Request roster upon login."""
        self.server = event.authorized_jid.bare()
        if "versioning" in self.server_features:
            if self.roster is not None and self.roster.version is not None:
                version = self.roster.version
            else:
                version = u""
        else:
            version = None
        self.request_roster(version)