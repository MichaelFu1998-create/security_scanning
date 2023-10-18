def _export_python(self, filename, **kwargs):
        """Pickle the Grid object

        The object is dumped as a dictionary with grid and edges: This
        is sufficient to recreate the grid object with __init__().
        """
        data = dict(grid=self.grid, edges=self.edges, metadata=self.metadata)
        with open(filename, 'wb') as f:
            cPickle.dump(data, f, cPickle.HIGHEST_PROTOCOL)