def allocate_colors(self, eps = 0.01, noise_size = 1):
        """!
        @brief Allocates color segments.
        
        @param[in] eps (double): Tolerance level that define maximal difference between phases of oscillators in one segment.
        @param[in] noise_size (uint): Threshold that defines noise - segments size (in pixels) that is less then the threshold is considered as a noise.
        
        @return (list) Color segments where each color segment consists of indexes of pixels that forms color segment.
        
        """
        
        segments = self.__color_analyser.allocate_clusters(eps);
        real_segments = [cluster for cluster in segments if len(cluster) > noise_size];
        return real_segments;