def som_create(rows, cols, conn_type, parameters):
    """!
    @brief Create of self-organized map using CCORE pyclustering library.
    
    @param[in] rows (uint): Number of neurons in the column (number of rows).
    @param[in] cols (uint): Number of neurons in the row (number of columns).
    @param[in] conn_type (type_conn): Type of connection between oscillators in the network (grid four, grid eight, honeycomb, function neighbour).
    @param[in] parameters (som_parameters): Other specific parameters.
    
    @return (POINTER) C-pointer to object of self-organized feature in memory.
    
    """  

    ccore = ccore_library.get()
    
    c_params = c_som_parameters()
    
    c_params.init_type = parameters.init_type
    c_params.init_radius = parameters.init_radius
    c_params.init_learn_rate = parameters.init_learn_rate
    c_params.adaptation_threshold = parameters.adaptation_threshold
    
    ccore.som_create.restype = POINTER(c_void_p)
    som_pointer = ccore.som_create(c_uint(rows), c_uint(cols), c_uint(conn_type), pointer(c_params))
    
    return som_pointer