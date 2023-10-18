def som_get_winner_number(som_pointer):
    """!
    @brief Returns of number of winner at the last step of learning process.
    
    @param[in] som_pointer (c_pointer): pointer to object of self-organized map.
    
    """
    
    ccore = ccore_library.get()
    ccore.som_get_winner_number.restype = c_size_t
    return ccore.som_get_winner_number(som_pointer)