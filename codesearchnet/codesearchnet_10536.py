def voronoi_from_pixel_centers(pixel_centers):
        """Compute the Voronoi grid of the pixelization, using the pixel centers.

        Parameters
        ----------
        pixel_centers : ndarray
            The (y,x) centre of every Voronoi pixel.
        """
        return scipy.spatial.Voronoi(np.asarray([pixel_centers[:, 1], pixel_centers[:, 0]]).T,
                                     qhull_options='Qbb Qc Qx Qm')