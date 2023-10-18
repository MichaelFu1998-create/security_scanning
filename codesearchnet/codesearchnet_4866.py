def __analyse_objects(self, image_source, color_analyser, collect_dynamic):
        """!
        @brief Performs object segmentation by the second layer.
        
        @param[in] image_source (string): Path to image file that should be processed.
        @param[in] color_analyser (syncnet_analyser): Analyser of color segmentation results.
        @param[in] collect_dynamic (bool): If 'True' then whole dynamic of the first layer of the network is collected.
        
        @return (map) Analysers of object segments.
        
        """
        
        # continue analysis
        pointer_image = Image.open(image_source);
        image_size = pointer_image.size;
        
        object_analysers = [];
        
        color_segments = color_analyser.allocate_clusters();
        
        for segment in color_segments:
            object_analyser = self.__analyse_color_segment(image_size, segment, collect_dynamic);
            if (object_analyser is not None):
                object_analysers.append( { 'color_segment': segment, 'analyser': object_analyser } );
    
        pointer_image.close();
        return object_analysers;