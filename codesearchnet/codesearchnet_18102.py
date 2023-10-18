def set_shape(self, shape, inner):
        """ Set the shape for all components """
        for c in self.comps:
            c.set_shape(shape, inner)