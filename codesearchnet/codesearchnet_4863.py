def allocate_objects(self, eps = 0.01, noise_size = 1):
        """!
        @brief Allocates object segments.
        
        @param[in] eps (double): Tolerance level that define maximal difference between phases of oscillators in one segment.
        @param[in] noise_size (uint): Threshold that defines noise - segments size (in pixels) that is less then the threshold is considered as a noise.
        
        @return (list) Object segments where each object segment consists of indexes of pixels that forms object segment.
        
        """
        
        if (self.__object_segment_analysers is None):
            return [];
        
        segments = [];
        for object_segment_analyser in self.__object_segment_analysers:
            indexes = object_segment_analyser['color_segment'];
            analyser = object_segment_analyser['analyser'];
            
            segments += analyser.allocate_clusters(eps, indexes);
        
        real_segments = [segment for segment in segments if len(segment) > noise_size];
        return real_segments;