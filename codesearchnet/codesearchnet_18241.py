def remove_user_from_acl(self, name, user):
        """Remove a user from the given acl (both allow and deny)."""
        if name not in self._acl:
            return False
        if user in self._acl[name]['allow']:
            self._acl[name]['allow'].remove(user)
        if user in self._acl[name]['deny']:
            self._acl[name]['deny'].remove(user)
        return True