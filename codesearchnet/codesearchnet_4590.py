def linear_sum(list_vector):
    """!
    @brief Calculates linear sum of vector that is represented by list, each element can be represented by list - multidimensional elements.
    
    @param[in] list_vector (list): Input vector.
    
    @return (list|double) Linear sum of vector that can be represented by list in case of multidimensional elements.
    
    """
    dimension = 1;
    linear_sum = 0.0;
    list_representation = (type(list_vector[0]) == list);
    
    if (list_representation is True):
        dimension = len(list_vector[0]);
        linear_sum = [0] * dimension;
        
    for index_element in range(0, len(list_vector)):
        if (list_representation is True):
            for index_dimension in range(0, dimension):
                linear_sum[index_dimension] += list_vector[index_element][index_dimension];
        else:
            linear_sum += list_vector[index_element];

    return linear_sum;