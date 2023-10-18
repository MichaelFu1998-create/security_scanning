def neighbors_from_pixelization(self, pixels, ridge_points):
        """Compute the neighbors of every Voronoi pixel as an ndarray of the pixel index's each pixel shares a \
        vertex with.

        The ridge points of the Voronoi grid are used to derive this.

        Parameters
        ----------
        ridge_points : scipy.spatial.Voronoi.ridge_points
            Each Voronoi-ridge (two indexes representing a pixel mapping_matrix).
        """
        return pixelization_util.voronoi_neighbors_from_pixels_and_ridge_points(pixels=pixels,
                                                                                ridge_points=np.asarray(ridge_points))