def process(self, image_source, collect_dynamic = False, order_color = 0.9995, order_object = 0.999):
        """!
        @brief Performs image segmentation.
        
        @param[in] image_source (string): Path to image file that should be processed.
        @param[in] collect_dynamic (bool): If 'True' then whole dynamic of each layer of the network is collected.
        @param[in] order_color (double): Local synchronization order for the first layer - coloring segmentation.
        @param[in] order_object (double): Local synchronization order for the second layer - object segmentation.
        
        @return (syncsegm_analyser) Analyser of segmentation results by the network.
        
        """
        
        self.__order_color  = order_color
        self.__order_object = order_object
        
        data = read_image(image_source)
        color_analyser = self.__analyse_colors(data, collect_dynamic)
        
        if self.__object_radius is None:
            return syncsegm_analyser(color_analyser, None)
    
        object_segment_analysers = self.__analyse_objects(image_source, color_analyser, collect_dynamic)
        return syncsegm_analyser(color_analyser, object_segment_analysers)