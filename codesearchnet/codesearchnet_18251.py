def load_user_rights(self, user):
        """Sets permissions on user object"""
        if user.username in self.admins:
            user.is_admin = True
        elif not hasattr(user, 'is_admin'):
            user.is_admin = False