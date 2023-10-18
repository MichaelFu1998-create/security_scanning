def exempt(self, resource):
        """Exempt a view function from being checked permission

        :param resource: The view function exempt from checking.
        """
        if resource not in self._exempt:
            self._exempt.append(resource)