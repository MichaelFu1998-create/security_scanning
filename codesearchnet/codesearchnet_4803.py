def som_get_capture_objects(som_pointer):
    """!
    @brief Returns list of indexes of captured objects by each neuron.
    
    @param[in] som_pointer (c_pointer): pointer to object of self-organized map.
    
    """
    
    ccore = ccore_library.get()
    
    ccore.som_get_capture_objects.restype = POINTER(pyclustering_package)
    package = ccore.som_get_capture_objects(som_pointer)
    
    result = package_extractor(package).extract()
    return result