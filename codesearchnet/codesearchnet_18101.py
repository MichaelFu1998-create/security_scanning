def get(self):
        """ Combine the fields from all components """
        fields = [c.get() for c in self.comps]
        return self.field_reduce_func(fields)