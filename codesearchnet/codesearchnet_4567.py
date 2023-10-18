def read_image(filename):
    """!
    @brief Returns image as N-dimension (depends on the input image) matrix, where one element of list describes pixel.
    
    @param[in] filename (string): Path to image.
    
    @return (list) Pixels where each pixel described by list of RGB-values.
    
    """
    
    with Image.open(filename) as image_source:
        data = [list(pixel) for pixel in image_source.getdata()]
        return data