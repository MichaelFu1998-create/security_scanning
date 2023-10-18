def read_sample(filename):
    """!
    @brief Returns data sample from simple text file.
    @details This function should be used for text file with following format:
    @code
    point_1_coord_1 point_1_coord_2 ... point_1_coord_n
    point_2_coord_1 point_2_coord_2 ... point_2_coord_n
    ... ...
    @endcode
    
    @param[in] filename (string): Path to file with data.
    
    @return (list) Points where each point represented by list of coordinates.
    
    """
    
    file = open(filename, 'r')

    sample = [[float(val) for val in line.split()] for line in file if len(line.strip()) > 0]
    
    file.close()
    return sample