def list_math_multiplication_number(a, b):
    """!
    @brief Multiplication between list and number.
    @details Each element from list 'a' is multiplied by number 'b'.
    
    @param[in] a (list): List of elements that supports mathematic division.
    @param[in] b (double): Number that supports mathematic division.
    
    @return (list) Result of division between list and number.
    
    """    
    return [a[i] * b for i in range(len(a))];