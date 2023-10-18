def show_distance_matrix(self):
        """!
        @brief Shows gray visualization of U-matrix (distance matrix).
        
        @see get_distance_matrix()
        
        """
        distance_matrix = self.get_distance_matrix()
        
        plt.imshow(distance_matrix, cmap = plt.get_cmap('hot'), interpolation='kaiser')
        plt.title("U-Matrix")
        plt.colorbar()
        plt.show()