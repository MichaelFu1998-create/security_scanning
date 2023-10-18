def get_password(self, service, username):
        """Get password of the username for the service
        """
        if not self.connected(service):
            # the user pressed "cancel" when prompted to unlock their keyring.
            raise KeyringLocked("Failed to unlock the keyring!")
        if not self.iface.hasEntry(self.handle, service, username, self.appid):
            return None
        password = self.iface.readPassword(
            self.handle, service, username, self.appid)
        return str(password)