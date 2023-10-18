def create(self, stylename, **kwargs):
        """ Creates a new style which inherits from the default style,
        or any other style which name is supplied to the optional template parameter.
        """
        if stylename == "default":    
            self[stylename] = style(stylename, self._ctx, **kwargs)
            return self[stylename]
        k = kwargs.get("template", "default")
        s = self[stylename] = self[k].copy(stylename)
        for attr in kwargs:
            if s.__dict__.has_key(attr):
                s.__dict__[attr] = kwargs[attr]
        return s