def list_math_multiplication(a, b):
    """!
    @brief Multiplication of two lists.
    @details Each element from list 'a' is multiplied by element from list 'b' accordingly.
    
    @param[in] a (list): List of elements that supports mathematic multiplication.
    @param[in] b (list): List of elements that supports mathematic multiplication.
    
    @return (list) Result of multiplication of elements in two lists.
    
    """        
    return [a[i] * b[i] for i in range(len(a))];