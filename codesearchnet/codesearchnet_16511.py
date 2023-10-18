def histogramdd(self):
        """Return array data as (edges,grid), i.e. a numpy nD histogram."""
        shape = self.components['positions'].shape
        edges = self.components['positions'].edges()
        hist = self.components['data'].array.reshape(shape)
        return (hist,edges)