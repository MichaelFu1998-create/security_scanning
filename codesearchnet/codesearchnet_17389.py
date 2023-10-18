def _match(self, **kwargs):
        """Method which indicates if the object matches specified criteria.

        Match accepts criteria as kwargs and looks them up on attributes.
        Actual matching is performed with fnmatch, so shell-like wildcards
        work within match strings. Examples:

        obj._match(AXTitle='Terminal*')
        obj._match(AXRole='TextField', AXRoleDescription='search text field')
        """
        for k in kwargs.keys():
            try:
                val = getattr(self, k)
            except _a11y.Error:
                return False
            # Not all values may be strings (e.g. size, position)
            if sys.version_info[:2] <= (2, 6):
                if isinstance(val, basestring):
                    if not fnmatch.fnmatch(unicode(val), kwargs[k]):
                        return False
                else:
                    if val != kwargs[k]:
                        return False
            elif sys.version_info[0] == 3:
                if isinstance(val, str):
                    if not fnmatch.fnmatch(val, str(kwargs[k])):
                        return False
                else:
                    if val != kwargs[k]:
                        return False
            else:
                if isinstance(val, str) or isinstance(val, unicode):
                    if not fnmatch.fnmatch(val, kwargs[k]):
                        return False
                else:
                    if val != kwargs[k]:
                        return False
        return True