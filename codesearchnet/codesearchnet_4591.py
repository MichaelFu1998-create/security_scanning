def square_sum(list_vector):
    """!
    @brief Calculates square sum of vector that is represented by list, each element can be represented by list - multidimensional elements.
    
    @param[in] list_vector (list): Input vector.
    
    @return (double) Square sum of vector.
    
    """
    
    square_sum = 0.0;
    list_representation = (type(list_vector[0]) == list);
        
    for index_element in range(0, len(list_vector)):
        if (list_representation is True):
            square_sum += sum(list_math_multiplication(list_vector[index_element], list_vector[index_element]));
        else:
            square_sum += list_vector[index_element] * list_vector[index_element];
         
    return square_sum;