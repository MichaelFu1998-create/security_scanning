def __extract_location_coordinates(self, image_size, color_segment):
        """!
        @brief Extracts coordinates of specified image segment.
        
        @param[in] image_size (list): Image size presented as a [width x height].
        @param[in] color_segment (list): Image segment whose coordinates should be extracted.
        
        @return (list) Coordinates of each pixel.
        
        """
        coordinates = [];
        for index in color_segment:
            y = floor(index / image_size[0]);
            x = index - y * image_size[0];
            
            coordinates.append([x, y]);
        
        return coordinates;