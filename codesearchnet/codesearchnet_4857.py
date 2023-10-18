def segmentation_image_simple1():
    "Perfect"
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
    
    template_segmentation_image(IMAGE_SIMPLE_SAMPLES.IMAGE_SIMPLE12, parameters, 2000, 2000, True);