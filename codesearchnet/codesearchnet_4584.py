def draw_clusters(data, clusters, noise = [], marker_descr = '.', hide_axes = False, axes = None, display_result = True):
    """!
    @brief Displays clusters for data in 2D or 3D.
    
    @param[in] data (list): Points that are described by coordinates represented.
    @param[in] clusters (list): Clusters that are represented by lists of indexes where each index corresponds to point in data.
    @param[in] noise (list): Points that are regarded to noise.
    @param[in] marker_descr (string): Marker for displaying points.
    @param[in] hide_axes (bool): If True - axes is not displayed.
    @param[in] axes (ax) Matplotlib axes where clusters should be drawn, if it is not specified (None) then new plot will be created.
    @param[in] display_result (bool): If specified then matplotlib axes will be used for drawing and plot will not be shown.
    
    @return (ax) Matplotlib axes where drawn clusters are presented.
    
    """
    # Get dimension
    dimension = 0;
    if ( (data is not None) and (clusters is not None) ):
        dimension = len(data[0]);
    elif ( (data is None) and (clusters is not None) ):
        dimension = len(clusters[0][0]);
    else:
        raise NameError('Data or clusters should be specified exactly.');
    
    "Draw clusters"
    colors = [ 'red', 'blue', 'darkgreen', 'brown', 'violet', 
               'deepskyblue', 'darkgrey', 'lightsalmon', 'deeppink', 'yellow',
               'black', 'mediumspringgreen', 'orange', 'darkviolet', 'darkblue',
               'silver', 'lime', 'pink', 'gold', 'bisque' ];
               
    if (len(clusters) > len(colors)):
        raise NameError('Impossible to represent clusters due to number of specified colors.');
    
    fig = plt.figure();
    
    if (axes is None):
        # Check for dimensions
        if ((dimension) == 1 or (dimension == 2)):
            axes = fig.add_subplot(111);
        elif (dimension == 3):
            axes = fig.gca(projection='3d');
        else:
            raise NameError('Drawer supports only 2d and 3d data representation');
    
    color_index = 0;
    for cluster in clusters:
        color = colors[color_index];
        for item in cluster:
            if (dimension == 1):
                if (data is None):
                    axes.plot(item[0], 0.0, color = color, marker = marker_descr);
                else:
                    axes.plot(data[item][0], 0.0, color = color, marker = marker_descr);
            
            if (dimension == 2):
                if (data is None):
                    axes.plot(item[0], item[1], color = color, marker = marker_descr);
                else:
                    axes.plot(data[item][0], data[item][1], color = color, marker = marker_descr);
                    
            elif (dimension == 3):
                if (data is None):
                    axes.scatter(item[0], item[1], item[2], c = color, marker = marker_descr);
                else:
                    axes.scatter(data[item][0], data[item][1], data[item][2], c = color, marker = marker_descr);
        
        color_index += 1;
    
    for item in noise:
        if (dimension == 1):
            if (data is None):
                axes.plot(item[0], 0.0, 'w' + marker_descr);
            else:
                axes.plot(data[item][0], 0.0, 'w' + marker_descr);

        if (dimension == 2):
            if (data is None):
                axes.plot(item[0], item[1], 'w' + marker_descr);
            else:
                axes.plot(data[item][0], data[item][1], 'w' + marker_descr);
                
        elif (dimension == 3):
            if (data is None):
                axes.scatter(item[0], item[1], item[2], c = 'w', marker = marker_descr);
            else:
                axes.scatter(data[item][0], data[item][1], data[item][2], c = 'w', marker = marker_descr);
    
    axes.grid(True);
    
    if (hide_axes is True):
        axes.xaxis.set_ticklabels([]);
        axes.yaxis.set_ticklabels([]);
        
        if (dimension == 3):
            axes.zaxis.set_ticklabels([]);
    
    if (display_result is True):
        plt.show();

    return axes;