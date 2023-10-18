def twenty_five_neurons_mix_stimulated():
    "Object allocation"
    "If M = 0 then only object will be allocated"
    params = pcnn_parameters();
    
    params.AF = 0.1;
    params.AL = 0.0;
    params.AT = 0.7;
    params.VF = 1.0;
    params.VL = 1.0;
    params.VT = 10.0;
    params.M = 0.0;
    
    template_dynamic_pcnn(25, 100, [0, 0, 0, 0, 0, 
                                    0, 0, 0, 0, 0,
                                    0, 1, 1, 0, 0,
                                    0, 1, 1, 0, 0,
                                    0, 0, 0, 0, 0], params, conn_type.GRID_FOUR, False);