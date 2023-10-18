def edges(self):
        """Edges of the grid cells, origin at centre of 0,0,..,0 grid cell.

        Only works for regular, orthonormal grids.
        """
        return [self.delta[d,d] * numpy.arange(self.shape[d]+1) + self.origin[d]\
                - 0.5*self.delta[d,d]     for d in range(self.rank)]