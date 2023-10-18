def is_denied(self, role, method, resource):
        """Check wherther role is denied to access resource

        :param role: Role to be checked.
        :param method: Method to be checked.
        :param resource: View function to be checked.
        """
        return (role, method, resource) in self._denied