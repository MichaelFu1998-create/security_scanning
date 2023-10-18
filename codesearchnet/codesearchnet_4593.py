def list_math_substraction_number(a, b):
    """!
    @brief Calculates subtraction between list and number.
    @details Each element from list 'a' is subtracted by number 'b'.
    
    @param[in] a (list): List of elements that supports mathematical subtraction.
    @param[in] b (list): Value that supports mathematical subtraction.
    
    @return (list) Results of subtraction between list and number.
    
    """        
    return [a[i] - b for i in range(len(a))];