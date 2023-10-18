def draw_dynamics(t, dyn, x_title = None, y_title = None, x_lim = None, y_lim = None, x_labels = True, y_labels = True, separate = False, axes = None):
    """!
    @brief Draw dynamics of neurons (oscillators) in the network.
    @details It draws if matplotlib is not specified (None), othewise it should be performed manually.
    
    @param[in] t (list): Values of time (used by x axis).
    @param[in] dyn (list): Values of output of oscillators (used by y axis).
    @param[in] x_title (string): Title for Y.
    @param[in] y_title (string): Title for X.
    @param[in] x_lim (double): X limit.
    @param[in] y_lim (double): Y limit.
    @param[in] x_labels (bool): If True - shows X labels.
    @param[in] y_labels (bool): If True - shows Y labels.
    @param[in] separate (list): Consists of lists of oscillators where each such list consists of oscillator indexes that will be shown on separated stage.
    @param[in] axes (ax): If specified then matplotlib axes will be used for drawing and plot will not be shown.
    
    @return (ax) Axes of matplotlib.
    
    """
         
    number_lines = 0;
    
    stage_xlim = None;
    if (x_lim is not None):
        stage_xlim = x_lim;
    elif (len(t) > 0):
        stage_xlim = [0, t[len(t) - 1]];
    
    if ( (isinstance(separate, bool) is True) and (separate is True) ):
        if (isinstance(dyn[0], list) is True):
            number_lines = len(dyn[0]);
        else:
            number_lines = 1;
            
    elif (isinstance(separate, list) is True):
        number_lines = len(separate);
        
    else:
        number_lines = 1;
    
    dysplay_result = False;
    if (axes is None):
        dysplay_result = True;
        (fig, axes) = plt.subplots(number_lines, 1);
    
    # Check if we have more than one dynamic
    if (isinstance(dyn[0], list) is True):
        num_items = len(dyn[0]);
        for index in range(0, num_items, 1):
            y = [item[index] for item in dyn];
            
            if (number_lines > 1):
                index_stage = -1;
                
                # Find required axes for the y
                if (isinstance(separate, bool) is True):
                    index_stage = index;
                    
                elif (isinstance(separate, list) is True):
                    for index_group in range(0, len(separate), 1):
                        if (index in separate[index_group]): 
                            index_stage = index_group;
                            break;
                
                if (index_stage != -1):
                    if (index_stage != number_lines - 1):
                        axes[index_stage].get_xaxis().set_visible(False);
                              
                    axes[index_stage].plot(t, y, 'b-', linewidth = 0.5); 
                    set_ax_param(axes[index_stage], x_title, y_title, stage_xlim, y_lim, x_labels, y_labels, True);
                
            else:
                axes.plot(t, y, 'b-', linewidth = 0.5);
                set_ax_param(axes, x_title, y_title, stage_xlim, y_lim, x_labels, y_labels, True);
    else:
        axes.plot(t, dyn, 'b-', linewidth = 0.5);
        set_ax_param(axes, x_title, y_title, stage_xlim, y_lim, x_labels, y_labels, True);
    
    if (dysplay_result is True):
        plt.show();
    
    return axes;