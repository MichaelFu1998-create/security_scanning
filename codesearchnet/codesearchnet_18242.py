def create_acl(self, name):
        """Create a new acl."""
        if name in self._acl:
            return False

        self._acl[name] = {
            'allow': [],
            'deny': []
        }
        return True