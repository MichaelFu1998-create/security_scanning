def show_network(self, awards = False, belongs = False, coupling = True, dataset = True, marker_type = 'o'):
        """!
        @brief Shows neurons in the dimension of data.
        
        @param[in] awards (bool): If True - displays how many objects won each neuron.
        @param[in] belongs (bool): If True - marks each won object by according index of neuron-winner (only when dataset is displayed too).
        @param[in] coupling (bool): If True - displays connections between neurons (except case when function neighbor is used).
        @param[in] dataset (bool): If True - displays inputs data set.
        @param[in] marker_type (string): Defines marker that is used for dispaying neurons in the network.
        
        """
        
        if self.__ccore_som_pointer is not None:
            self._size = wrapper.som_get_size(self.__ccore_som_pointer)
            self._weights = wrapper.som_get_weights(self.__ccore_som_pointer)
            self._neighbors = wrapper.som_get_neighbors(self.__ccore_som_pointer)
            self._award = wrapper.som_get_awards(self.__ccore_som_pointer)

        dimension = len(self._weights[0])
        
        fig = plt.figure()
        
        # Check for dimensions
        if (dimension == 1) or (dimension == 2):
            axes = fig.add_subplot(111)
        elif dimension == 3:
            axes = fig.gca(projection='3d')
        else:
            raise NotImplementedError('Impossible to show network in data-space that is differ from 1D, 2D or 3D.')

        if (self._data is not None) and (dataset is True):
            for x in self._data:
                if dimension == 1:
                    axes.plot(x[0], 0.0, 'b|', ms = 30)
                    
                elif dimension == 2:
                    axes.plot(x[0], x[1], 'b.')
                    
                elif dimension == 3:
                    axes.scatter(x[0], x[1], x[2], c = 'b', marker = '.')
        
        # Show neurons
        for index in range(self._size):
            color = 'g'
            if self._award[index] == 0:
                color = 'y'
            
            if dimension == 1:
                axes.plot(self._weights[index][0], 0.0, color + marker_type)
                
                if awards:
                    location = '{0}'.format(self._award[index])
                    axes.text(self._weights[index][0], 0.0, location, color='black', fontsize = 10)
            
                if belongs and self._data is not None:
                    location = '{0}'.format(index)
                    axes.text(self._weights[index][0], 0.0, location, color='black', fontsize = 12)
                    for k in range(len(self._capture_objects[index])):
                        point = self._data[self._capture_objects[index][k]]
                        axes.text(point[0], 0.0, location, color='blue', fontsize = 10)
            
            if dimension == 2:
                axes.plot(self._weights[index][0], self._weights[index][1], color + marker_type)
                
                if awards:
                    location = '{0}'.format(self._award[index])
                    axes.text(self._weights[index][0], self._weights[index][1], location, color='black', fontsize=10)
                    
                if belongs and self._data is not None:
                    location = '{0}'.format(index)
                    axes.text(self._weights[index][0], self._weights[index][1], location, color='black', fontsize=12)
                    for k in range(len(self._capture_objects[index])):
                        point = self._data[self._capture_objects[index][k]]
                        axes.text(point[0], point[1], location, color='blue', fontsize=10)
                
                if (self._conn_type != type_conn.func_neighbor) and (coupling != False):
                    for neighbor in self._neighbors[index]:
                        if neighbor > index:
                            axes.plot([self._weights[index][0], self._weights[neighbor][0]],
                                      [self._weights[index][1], self._weights[neighbor][1]],
                                      'g', linewidth=0.5)
            
            elif dimension == 3:
                axes.scatter(self._weights[index][0], self._weights[index][1], self._weights[index][2], c=color, marker=marker_type)
                
                if (self._conn_type != type_conn.func_neighbor) and (coupling != False):
                    for neighbor in self._neighbors[index]:
                        if neighbor > index:
                            axes.plot([self._weights[index][0], self._weights[neighbor][0]],
                                      [self._weights[index][1], self._weights[neighbor][1]],
                                      [self._weights[index][2], self._weights[neighbor][2]],
                                      'g-', linewidth=0.5)

        plt.title("Network Structure")
        plt.grid()
        plt.show()