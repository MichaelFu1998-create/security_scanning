def set_ax_param(ax, x_title = None, y_title = None, x_lim = None, y_lim = None, x_labels = True, y_labels = True, grid = True):
    """!
    @brief Sets parameters for matplotlib ax.
    
    @param[in] ax (Axes): Axes for which parameters should applied.
    @param[in] x_title (string): Title for Y.
    @param[in] y_title (string): Title for X.
    @param[in] x_lim (double): X limit.
    @param[in] y_lim (double): Y limit.
    @param[in] x_labels (bool): If True - shows X labels.
    @param[in] y_labels (bool): If True - shows Y labels.
    @param[in] grid (bool): If True - shows grid.
    
    """
    from matplotlib.font_manager import FontProperties;
    from matplotlib import rcParams;
    
    if (_platform == "linux") or (_platform == "linux2"):
        rcParams['font.sans-serif'] = ['Liberation Serif'];
    else:
        rcParams['font.sans-serif'] = ['Arial'];
        
    rcParams['font.size'] = 12;
        
    surface_font = FontProperties();
    if (_platform == "linux") or (_platform == "linux2"):
        surface_font.set_name('Liberation Serif');
    else:
        surface_font.set_name('Arial');
        
    surface_font.set_size('12');
    
    if (y_title is not None): ax.set_ylabel(y_title, fontproperties = surface_font);
    if (x_title is not None): ax.set_xlabel(x_title, fontproperties = surface_font);
    
    if (x_lim is not None): ax.set_xlim(x_lim[0], x_lim[1]);
    if (y_lim is not None): ax.set_ylim(y_lim[0], y_lim[1]);
    
    if (x_labels is False): ax.xaxis.set_ticklabels([]);
    if (y_labels is False): ax.yaxis.set_ticklabels([]);
    
    ax.grid(grid);