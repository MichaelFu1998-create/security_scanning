def norm_vector(vector):
    """!
    @brief Calculates norm of an input vector that is known as a vector length.
    
    @param[in] vector (list): The input vector whose length is calculated.
    
    @return (double) vector norm known as vector length.
    
    """
    
    length = 0.0
    for component in vector:
        length += component * component
    
    length = length ** 0.5
    
    return length