def show_winner_matrix(self):
        """!
        @brief Show winner matrix where each element corresponds to neuron and value represents
               amount of won objects from input dataspace at the last training iteration.
        
        @see show_distance_matrix()
        
        """
        
        if self.__ccore_som_pointer is not None:
            self._award = wrapper.som_get_awards(self.__ccore_som_pointer)
        
        (fig, ax) = plt.subplots()
        winner_matrix = [[0] * self._cols for i in range(self._rows)]
        
        for i in range(self._rows):
            for j in range(self._cols):
                neuron_index = i * self._cols + j
                
                winner_matrix[i][j] = self._award[neuron_index]
                ax.text(i, j, str(winner_matrix[i][j]), va='center', ha='center')
        
        ax.imshow(winner_matrix, cmap = plt.get_cmap('cool'), interpolation='none')
        ax.grid(True)
        
        plt.title("Winner Matrix")
        plt.show()