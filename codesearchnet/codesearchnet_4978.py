def show_density_matrix(self, surface_divider = 20.0):
        """!
        @brief Show density matrix (P-matrix) using kernel density estimation.
        
        @param[in] surface_divider (double): Divider in each dimension that affect radius for density measurement.
        
        @see show_distance_matrix()
        
        """
        density_matrix = self.get_density_matrix(surface_divider)
        
        plt.imshow(density_matrix, cmap = plt.get_cmap('hot'), interpolation='kaiser')
        plt.title("P-Matrix")
        plt.colorbar()
        plt.show()