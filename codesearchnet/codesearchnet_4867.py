def __analyse_color_segment(self, image_size, color_segment, collect_dynamic):
        """!
        @brief Performs object segmentation of separate segment.
        
        @param[in] image_size (list): Image size presented as a [width x height].
        @param[in] color_segment (list): Image segment that should be processed.
        @param[in] collect_dynamic (bool): If 'True' then whole dynamic of the second layer of the network is collected.
        
        @return (syncnet_analyser) Analyser of object segmentation results of the second layer.
        
        """
        coordinates = self.__extract_location_coordinates(image_size, color_segment);
        
        if (len(coordinates) < self.__noise_size):
            return None;
        
        network = syncnet(coordinates, self.__object_radius, initial_phases = initial_type.EQUIPARTITION, ccore = True);
        analyser = network.process(self.__order_object, solve_type.FAST, collect_dynamic);
        
        return analyser;