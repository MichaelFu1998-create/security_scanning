def _rc_mset(self, mapping):
        "Sets each key in the ``mapping`` dict to its corresponding value"
        result = True
        for k, v in iteritems(mapping):
            result = result and self.set(k, v)
        return result