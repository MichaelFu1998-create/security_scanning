def som_load(som_pointer, weights, award, capture_objects):
    """!
    @brief Load dump of the network to SOM.
    @details Initialize SOM using existed weights, amount of captured objects by each neuron, captured
              objects by each neuron. Initialization is not performed if weights are empty.

    @param[in] som_pointer (POINTER): pointer to object of self-organized map.
    @param[in] weights (list): weights that should assigned to neurons.
    @param[in] awards (list): amount of captured objects by each neuron.
    @param[in] capture_objects (list): captured objects by each neuron.

    """

    if len(weights) == 0:
        return

    ccore = ccore_library.get()

    package_weights = package_builder(weights, c_double).create()
    package_award = package_builder(award, c_size_t).create()
    package_capture_objects = package_builder(capture_objects, c_size_t).create()

    ccore.som_load(som_pointer, package_weights, package_award, package_capture_objects)