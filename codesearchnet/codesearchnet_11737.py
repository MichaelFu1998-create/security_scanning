def expire_password(self, username):
        """
        Forces the user to change their password the next time they login.
        """
        r = self.local_renderer
        r.env.username = username
        r.sudo('chage -d 0 {username}')