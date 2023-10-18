def list_math_addition_number(a, b):
    """!
    @brief Addition between list and number.
    @details Each element from list 'a' is added to number 'b'.
    
    @param[in] a (list): List of elements that supports mathematic addition.
    @param[in] b (double): Value that supports mathematic addition.
    
    @return (list) Result of addtion of two lists.
    
    """    
    return [a[i] + b for i in range(len(a))];