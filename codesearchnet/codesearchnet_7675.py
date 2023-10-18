def set_password(self, service, username, password):
        """Set password for the username of the service
        """
        if not self.connected(service):
            # the user pressed "cancel" when prompted to unlock their keyring.
            raise PasswordSetError("Cancelled by user")
        self.iface.writePassword(
            self.handle, service, username, password, self.appid)