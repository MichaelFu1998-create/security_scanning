def list_math_addition(a, b):
    """!
    @brief Addition of two lists.
    @details Each element from list 'a' is added to element from list 'b' accordingly.
    
    @param[in] a (list): List of elements that supports mathematic addition..
    @param[in] b (list): List of elements that supports mathematic addition..
    
    @return (list) Results of addtion of two lists.
    
    """    
    return [a[i] + b[i] for i in range(len(a))];