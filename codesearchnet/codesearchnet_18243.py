def delete_acl(self, name):
        """Delete an acl."""
        if name not in self._acl:
            return False

        del self._acl[name]
        return True