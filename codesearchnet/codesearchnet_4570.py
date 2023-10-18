def gray_pattern_borders(image):
    """!
    @brief Returns coordinates of gray image content on the input image.
    
    @param[in] image (Image): PIL Image instance that is processed.
    
    @return (tuple) Returns coordinates of gray image content as (width_start, height_start, width_end, height_end).
    
    """
    
    width, height = image.size;
    
    width_start = width;
    width_end = 0;
    height_start = height;
    height_end = 0;
    
    row, col = 0, 0;
    for pixel in image.getdata():
        value = float(pixel[0]) * 0.2989 + float(pixel[1]) * 0.5870 + float(pixel[2]) * 0.1140;
        
        if (value < 128):
            if (width_end < col): 
                width_end = col;
            
            if (height_end < row):
                height_end = row;
        
            if (width_start > col):
                width_start = col;
            
            if (height_start > row):
                height_start = row;
        
        col += 1;
        if (col >= width):
            col = 0;
            row += 1;

    return (width_start, height_start, width_end + 1, height_end + 1);