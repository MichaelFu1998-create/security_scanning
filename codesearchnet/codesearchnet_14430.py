def as_namespace(self, namespace=None):
        """
        Return this call as if it were being assigned in a pyconfig namespace.

        If `namespace` is specified and matches the top level of this call's
        :attr:`key`, then that section of the key will be removed.

        """
        key = self.key
        if namespace and key.startswith(namespace):
            key = key[len(namespace) + 1:]

        return "%s = %s" % (self.get_key(), self._default() or NotSet())