def sixteen_oscillator_two_stimulated_ensembles_grid():
    "Not accurate false due to spikes are observed"
    parameters = legion_parameters();
    parameters.teta_x = -1.1;
    template_dynamic_legion(16, 2000, 1500, conn_type = conn_type.GRID_FOUR, params = parameters, stimulus = [1, 1, 1, 0, 
                                                                                                              1, 1, 1, 0, 
                                                                                                              0, 0, 0, 1, 
                                                                                                              0, 0, 1, 1]);