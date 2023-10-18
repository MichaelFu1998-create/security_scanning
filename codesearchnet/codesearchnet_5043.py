def __create_weights_all_to_all(self, stimulus):
        """!
        @brief Create weight all-to-all structure between neurons in line with stimulus.
        
        @param[in] stimulus (list): External stimulus for the chaotic neural network.
        
        """
        
        for i in range(len(stimulus)):
            for j in range(i + 1, len(stimulus)):
                weight = self.__calculate_weight(stimulus[i], stimulus[j])
                
                self.__weights[i][j] = weight
                self.__weights[j][i] = weight
                
                self.__weights_summary[i] += weight
                self.__weights_summary[j] += weight