def list_math_division_number(a, b):
    """!
    @brief Division between list and number.
    @details Each element from list 'a' is divided by number 'b'.
    
    @param[in] a (list): List of elements that supports mathematic division.
    @param[in] b (double): Value that supports mathematic division.
    
    @return (list) Result of division between list and number.
    
    """    
    return [a[i] / b for i in range(len(a))];