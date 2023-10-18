def hundred_neurons_mix_stimulated():
    "Allocate several clusters: the first contains borders (indexes of oscillators) and the second objects (indexes of oscillators)"
    params = pcnn_parameters();
    
    params.AF = 0.1;
    params.AL = 0.1;
    params.AT = 0.8;
    params.VF = 1.0;
    params.VL = 1.0;
    params.VT = 20.0;
    params.W = 1.0;
    params.M = 1.0;
    
    template_dynamic_pcnn(100, 50,  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                                     0, 1, 1, 1, 0, 0, 0, 0, 0, 0,
                                     0, 1, 1, 1, 0, 0, 0, 0, 0, 0,
                                     0, 1, 1, 1, 0, 0, 0, 0, 0, 0,
                                     0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                                     0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                                     0, 0, 0, 0, 0, 1, 1, 1, 1, 0,
                                     0, 0, 0, 0, 0, 1, 1, 1, 1, 0,
                                     0, 0, 0, 0, 0, 1, 1, 1, 1, 0,
                                     0, 0, 0, 0, 0, 0, 0, 0, 0, 0], params, conn_type.GRID_EIGHT, False);