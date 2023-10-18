def is_allowed(self, role, method, resource):
        """Check whether role is allowed to access resource

        :param role: Role to be checked.
        :param method: Method to be checked.
        :param resource: View function to be checked.
        """
        return (role, method, resource) in self._allowed