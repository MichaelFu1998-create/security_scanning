def as_call(self):
        """
        Return this call as it is called in its source.

        """
        default = self._default()
        default = ', ' + default if default else ''
        return "pyconfig.%s(%r%s)" % (self.method, self.get_key(), default)