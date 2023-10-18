def _nsattr(self, attr, ns=None):
        ''' returns an attribute name w/ namespace prefix'''
        if ns is None:
            return attr
        return '{' + self._ns[ns] + '}' + attr