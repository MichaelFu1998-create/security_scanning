def __analyse_colors(self, image_data, collect_dynamic):
        """!
        @brief Performs color segmentation by the first layer.
        
        @param[in] image_data (array_like): Image sample as a array-like structure.
        @param[in] collect_dynamic (bool): If 'True' then whole dynamic of the first layer of the network is collected.
        
        @return (syncnet_analyser) Analyser of color segmentation results of the first layer.
        
        """
        
        network = syncnet(image_data, self.__color_radius, initial_phases = initial_type.RANDOM_GAUSSIAN, ccore = self.__ccore);
        analyser = network.process(self.__order_color, solve_type.FAST, collect_dynamic);
        
        return analyser;