def thirteen_simplify_oscillator_three_stimulated_ensembles_list():
    "Good example of three synchronous ensembels"
    "Not accurate due to false skipes are observed"
    parameters = legion_parameters();
    parameters.Wt = 4.0;
    parameters.fi = 0.8;
    parameters.ENABLE_POTENTIONAL = False;
    template_dynamic_legion(15, 1000, 1000, conn_type = conn_type.LIST_BIDIR, 
                            stimulus = [1, 1, 1, 0, 0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 1], 
                            params = parameters, 
                            separate_repr = [ [0, 1, 2], [3, 4, 5, 9, 10], [6, 7, 8], [11, 12, 13, 14] ]);