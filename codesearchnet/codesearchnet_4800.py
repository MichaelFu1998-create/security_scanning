def som_simulate(som_pointer, pattern):
    """!
    @brief Processes input pattern (no learining) and returns index of neuron-winner.
    @details Using index of neuron winner catched object can be obtained using property capture_objects.
    
    @param[in] som_pointer (c_pointer): pointer to object of self-organized map.
    @param[in] pattern (list): input pattern.
    
    @return Returns index of neuron-winner.
    
    """
    
    pointer_data = package_builder(pattern, c_double).create()
    
    ccore = ccore_library.get()
    ccore.som_simulate.restype = c_size_t
    return ccore.som_simulate(som_pointer, pointer_data)