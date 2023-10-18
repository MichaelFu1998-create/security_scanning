def access_ok(self, access):
        """ Check if there is enough permissions for access """
        for c in access:
            if c not in self.perms:
                return False
        return True