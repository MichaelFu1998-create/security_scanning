def simple_segmentation_example():
    "Perfect results!"
    parameters = legion_parameters();
    parameters.eps = 0.02;
    parameters.alpha = 0.005;
    parameters.betta = 0.1;
    parameters.gamma = 7.0;
    parameters.teta = 0.9;
    parameters.lamda = 0.1;
    parameters.teta_x = -0.5;
    parameters.teta_p = 7.0;
    parameters.Wz = 0.7;
    parameters.mu = 0.01;
    parameters.fi = 3.0;
    parameters.teta_xz = 0.1;
    parameters.teta_zx = 0.1;
    
    parameters.ENABLE_POTENTIONAL = False;
    template_dynamic_legion(81, 2500, 2500, 
                            conn_type = conn_type.GRID_FOUR, 
                            params = parameters, 
                            stimulus = [1, 1, 1, 0, 0, 0, 0, 0, 0, 
                                        1, 1, 1, 0, 0, 1, 1, 1, 1, 
                                        1, 1, 1, 0, 0, 1, 1, 1, 1, 
                                        0, 0, 0, 0, 0, 0, 1, 1, 1,
                                        0, 0, 0, 0, 0, 0, 1, 1, 1,
                                        1, 1, 1, 1, 0, 0, 1, 1, 1,
                                        1, 1, 1, 1, 0, 0, 0, 0, 0,
                                        1, 1, 1, 1, 0, 0, 0, 0, 0,
                                        1, 1, 1, 1, 0, 0, 0, 0, 0],
                            separate_repr = [ [0, 1, 2, 9, 10, 11, 18, 19, 20], 
                                              [14, 15, 16, 17, 23, 24, 25, 26, 33, 34, 35, 42, 43, 44, 51, 52, 53], 
                                              [45, 46, 47, 48, 54, 55, 56, 57, 63, 64, 65, 66, 72, 73, 74, 75] ]);