def draw_dynamics_set(dynamics, xtitle = None, ytitle = None, xlim = None, ylim = None, xlabels = False, ylabels = False):
    """!
    @brief Draw lists of dynamics of neurons (oscillators) in the network.
    
    @param[in] dynamics (list): List of network outputs that are represented by values of output of oscillators (used by y axis).
    @param[in] xtitle (string): Title for Y.
    @param[in] ytitle (string): Title for X.
    @param[in] xlim (double): X limit.
    @param[in] ylim (double): Y limit.
    @param[in] xlabels (bool): If True - shows X labels.
    @param[in] ylabels (bool): If True - shows Y labels.
    
    """
    # Calculate edge for confortable representation.
    number_dynamics = len(dynamics);
    if (number_dynamics == 1):
        draw_dynamics(dynamics[0][0], dynamics[0][1], xtitle, ytitle, xlim, ylim, xlabels, ylabels);
        return;
    
    number_cols = int(numpy.ceil(number_dynamics ** 0.5));
    number_rows = int(numpy.ceil(number_dynamics / number_cols));

    real_index = 0, 0;
    double_indexer = True;
    if ( (number_cols == 1) or (number_rows == 1) ):
        real_index = 0;
        double_indexer = False;
    
    (_, axarr) = plt.subplots(number_rows, number_cols);
    #plt.setp([ax for ax in axarr], visible = False);
    
    for dynamic in dynamics:
        axarr[real_index] = draw_dynamics(dynamic[0], dynamic[1], xtitle, ytitle, xlim, ylim, xlabels, ylabels, axes = axarr[real_index]);
        #plt.setp(axarr[real_index], visible = True);
        
        if (double_indexer is True):
            real_index = real_index[0], real_index[1] + 1;
            if (real_index[1] >= number_cols):
                real_index = real_index[0] + 1, 0; 
        else:
            real_index += 1;
            
    plt.show();