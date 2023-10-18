def rgb2gray(image_rgb_array):
    """!
    @brief Returns image as 1-dimension (gray colored) matrix, where one element of list describes pixel.
    @details Luma coding is used for transformation and that is calculated directly from gamma-compressed primary intensities as a weighted sum:
    
    \f[Y = 0.2989R + 0.587G + 0.114B\f]
    
    @param[in] image_rgb_array (list): Image represented by RGB list.
    
    @return (list) Image as gray colored matrix, where one element of list describes pixel.
    
    @code
        colored_image = read_image(file_name);
        gray_image = rgb2gray(colored_image);
    @endcode
    
    @see read_image()
    
    """
    
    image_gray_array = [0.0] * len(image_rgb_array);
    for index in range(0, len(image_rgb_array), 1):
        image_gray_array[index] = float(image_rgb_array[index][0]) * 0.2989 + float(image_rgb_array[index][1]) * 0.5870 + float(image_rgb_array[index][2]) * 0.1140;
    
    return image_gray_array;