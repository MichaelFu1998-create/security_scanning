def coords(self, norm=False, form='broadcast'):
        """
        Returns the coordinate vectors associated with the tile.

        Parameters
        -----------
        norm : boolean
            can rescale the coordinates for you. False is no rescaling, True is
            rescaling so that all coordinates are from 0 -> 1.  If a scalar,
            the same norm is applied uniformally while if an iterable, each
            scale is applied to each dimension.

        form : string
            In what form to return the vector array. Can be one of:
                'broadcast' -- return 1D arrays that are broadcasted to be 3D

                'flat' -- return array without broadcasting so each component
                    is 1D and the appropriate length as the tile

                'meshed' -- arrays are explicitly broadcasted and so all have
                    a 3D shape, each the size of the tile.

                'vector' -- array is meshed and combined into one array with
                    the vector components along last dimension [Nz, Ny, Nx, 3]

        Examples
        --------
        >>> Tile(3, dim=2).coords(form='meshed')[0]
        array([[ 0.,  0.,  0.],
               [ 1.,  1.,  1.],
               [ 2.,  2.,  2.]])

        >>> Tile(3, dim=2).coords(form='meshed')[1]
        array([[ 0.,  1.,  2.],
               [ 0.,  1.,  2.],
               [ 0.,  1.,  2.]])

        >>> Tile([4,5]).coords(form='vector').shape
        (4, 5, 2)

        >>> [i.shape for i in Tile((4,5), dim=2).coords(form='broadcast')]
        [(4, 1), (1, 5)]
        """
        if norm is False:
            norm = 1
        if norm is True:
            norm = np.array(self.shape)
        norm = aN(norm, self.dim, dtype='float')

        v = list(np.arange(self.l[i], self.r[i]) / norm[i] for i in range(self.dim))
        return self._format_vector(v, form=form)