def as_live(self):
        """
        Return this call as if it were being assigned in a pyconfig namespace,
        but load the actual value currently available in pyconfig.

        """
        key = self.get_key()
        default = pyconfig.get(key)
        if default:
            default = repr(default)
        else:
            default = self._default() or NotSet()
        return "%s = %s" % (key, default)