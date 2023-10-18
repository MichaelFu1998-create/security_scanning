def som_get_size(som_pointer):
    """!
    @brief Returns size of self-organized map (number of neurons).
    
    @param[in] som_pointer (c_pointer): pointer to object of self-organized map.
    
    """
    
    ccore = ccore_library.get()
    ccore.som_get_size.restype = c_size_t
    return ccore.som_get_size(som_pointer)