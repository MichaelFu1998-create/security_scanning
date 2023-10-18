def map_attr(self, mapping, attr, obj):
        """
        A kind of cheesy method that allows for callables or attributes to
        be used interchangably
        """
        if attr not in mapping and hasattr(self, attr):
            if not callable(getattr(self, attr)):
                mapping[attr] = getattr(self, attr)
            else:
                mapping[attr] = getattr(self, attr)(obj)