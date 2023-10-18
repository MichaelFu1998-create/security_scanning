def get_refkey(self, obj, referent):
        """Return the dict key or attribute name of obj which refers to
        referent."""
        if isinstance(obj, dict):
            for k, v in obj.items():
                if v is referent:
                    return " (via its %r key)" % k

        for k in dir(obj) + ['__dict__']:
            if getattr(obj, k, None) is referent:
                return " (via its %r attribute)" % k
        return ""