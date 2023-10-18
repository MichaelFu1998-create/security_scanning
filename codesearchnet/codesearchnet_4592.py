def list_math_subtraction(a, b):
    """!
    @brief Calculates subtraction of two lists.
    @details Each element from list 'a' is subtracted by element from list 'b' accordingly.
    
    @param[in] a (list): List of elements that supports mathematical subtraction.
    @param[in] b (list): List of elements that supports mathematical subtraction.
    
    @return (list) Results of subtraction of two lists.
    
    """
    return [a[i] - b[i] for i in range(len(a))];