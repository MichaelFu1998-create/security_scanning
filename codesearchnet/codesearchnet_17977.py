def corners(self):
        """
        Iterate the vector of all corners of the hyperrectangles

        >>> Tile(3, dim=2).corners
        array([[0, 0],
               [0, 3],
               [3, 0],
               [3, 3]])
        """
        corners = []
        for ind in itertools.product(*((0,1),)*self.dim):
            ind = np.array(ind)
            corners.append(self.l + ind*self.r)
        return np.array(corners)