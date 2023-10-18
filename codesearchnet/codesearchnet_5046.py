def show_network(self):
        """!
        @brief Shows structure of the network: neurons and connections between them.
        
        """
        
        dimension = len(self.__location[0])
        if (dimension != 3) and (dimension != 2):
            raise NameError('Network that is located in different from 2-d and 3-d dimensions can not be represented')

        (fig, axes) = self.__create_surface(dimension)
        
        for i in range(0, self.__num_osc, 1):
            if dimension == 2:
                axes.plot(self.__location[i][0], self.__location[i][1], 'bo')
                for j in range(i, self.__num_osc, 1):    # draw connection between two points only one time
                    if self.__weights[i][j] > 0.0:
                        axes.plot([self.__location[i][0], self.__location[j][0]], [self.__location[i][1], self.__location[j][1]], 'b-', linewidth = 0.5)
            
            elif dimension == 3:
                axes.scatter(self.__location[i][0], self.__location[i][1], self.__location[i][2], c = 'b', marker = 'o')
                
                for j in range(i, self.__num_osc, 1):    # draw connection between two points only one time
                    if self.__weights[i][j] > 0.0:
                        axes.plot([self.__location[i][0], self.__location[j][0]], [self.__location[i][1], self.__location[j][1]], [self.__location[i][2], self.__location[j][2]], 'b-', linewidth = 0.5)
                
        plt.grid()
        plt.show()