def delete_password(self, service, username):
        """Delete the password for the username of the service.
        """
        if not self.connected(service):
            # the user pressed "cancel" when prompted to unlock their keyring.
            raise PasswordDeleteError("Cancelled by user")
        if not self.iface.hasEntry(self.handle, service, username, self.appid):
            raise PasswordDeleteError("Password not found")
        self.iface.removeEntry(self.handle, service, username, self.appid)