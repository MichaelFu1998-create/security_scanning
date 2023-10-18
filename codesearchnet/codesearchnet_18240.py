def add_user_to_allow(self, name, user):
        """Add a user to the given acl allow block."""

        # Clear user from both allow and deny before adding
        if not self.remove_user_from_acl(name, user):
            return False

        if name not in self._acl:
            return False

        self._acl[name]['allow'].append(user)
        return True