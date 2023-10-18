def _to_attrdict(self, attrs=None):
        """Get extra attributes"""
        result = self._baseattrs

        for attr in attrs:
            if hasattr(self, attr):
                result[attr] = getattr(self, attr)._to_attrdict(attrs)

        return result