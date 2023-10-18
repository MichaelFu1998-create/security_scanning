def stretch_pattern(image_source):
    """!
    @brief Returns stretched content as 1-dimension (gray colored) matrix with size of input image.
    
    @param[in] image_source (Image): PIL Image instance.
    
    @return (list, Image) Stretched image as gray colored matrix and source image.
    
    """
    wsize, hsize = image_source.size;
    
    # Crop digit exactly
    (ws, hs, we, he) = gray_pattern_borders(image_source);
    image_source = image_source.crop((ws, hs, we, he));
    
    # Stretch it to initial sizes
    image_source = image_source.resize((wsize, hsize), Image.ANTIALIAS);
    
    # Transform image to simple array
    data = [pixel for pixel in image_source.getdata()];
    image_pattern = rgb2gray(data);
    
    return (image_pattern, image_source);