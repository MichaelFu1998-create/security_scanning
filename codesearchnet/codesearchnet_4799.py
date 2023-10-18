def som_train(som_pointer, data, epochs, autostop):
    """!
    @brief Trains self-organized feature map (SOM) using CCORE pyclustering library.

    @param[in] data (list): Input data - list of points where each point is represented by list of features, for example coordinates.
    @param[in] epochs (uint): Number of epochs for training.        
    @param[in] autostop (bool): Automatic termination of learining process when adaptation is not occurred.
    
    @return (uint) Number of learining iterations.
    
    """ 
    
    pointer_data = package_builder(data, c_double).create()
    
    ccore = ccore_library.get()
    ccore.som_train.restype = c_size_t
    return ccore.som_train(som_pointer, pointer_data, c_uint(epochs), autostop)