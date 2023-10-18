def handle_authorized(self, event):
        """Send the initial presence after log-in."""
        request_software_version(self.client, self.target_jid,
                                        self.success, self.failure)