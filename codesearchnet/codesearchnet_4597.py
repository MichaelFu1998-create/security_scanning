def list_math_division(a, b):
    """!
    @brief Division of two lists.
    @details Each element from list 'a' is divided by element from list 'b' accordingly.
    
    @param[in] a (list): List of elements that supports mathematic division.
    @param[in] b (list): List of elements that supports mathematic division.
    
    @return (list) Result of division of two lists.
    
    """    
    return [a[i] / b[i] for i in range(len(a))];