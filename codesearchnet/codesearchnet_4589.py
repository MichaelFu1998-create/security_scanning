def draw_image_mask_segments(source, clusters, hide_axes = True):
    """!
    @brief Shows image segments using black masks.
    @details Each black mask of allocated segment is presented on separate plot.
             The first image is initial and others are black masks of segments.
    
    @param[in] source (string): Path to image.
    @param[in] clusters (list): List of clusters (allocated segments of image) where each cluster
                                consists of indexes of pixel from source image.
    @param[in] hide_axes (bool): If True then axes will not be displayed.
    
    """
    if (len(clusters) == 0):
        print("Warning: Nothing to draw - list of clusters is empty.")
        return;
        
    image_source = Image.open(source);
    image_size = image_source.size;
    
    # Calculate edge for confortable representation.
    number_clusters = len(clusters) + 1; # show with the source image
    
    number_cols = int(numpy.ceil(number_clusters ** 0.5));
    number_rows = int(numpy.ceil(number_clusters / number_cols));
    

    real_index = 0, 0;
    double_indexer = True;
    if ( (number_cols == 1) or (number_rows == 1) ):
        real_index = 0;
        double_indexer = False;
    
    (fig, axarr) = plt.subplots(number_rows, number_cols);
    plt.setp([ax for ax in axarr], visible = False);
    
    axarr[real_index].imshow(image_source, interpolation = 'none');
    plt.setp(axarr[real_index], visible = True);
    
    if (hide_axes is True):
        axarr[real_index].xaxis.set_ticklabels([]);
        axarr[real_index].yaxis.set_ticklabels([]);
        axarr[real_index].xaxis.set_ticks_position('none');
        axarr[real_index].yaxis.set_ticks_position('none');
            
    if (double_indexer is True):
        real_index = 0, 1;
    else:
        real_index += 1;
    
    for cluster in clusters:
        stage_cluster = [(255, 255, 255)] * (image_size[0] * image_size[1]);
        for index in cluster:
            stage_cluster[index] = (0, 0, 0);
          
        stage = array(stage_cluster, numpy.uint8);
        stage = numpy.reshape(stage, (image_size[1], image_size[0]) + ((3),)); # ((3),) it's size of RGB - third dimension.
        
        image_cluster = Image.fromarray(stage, 'RGB');
        
        axarr[real_index].imshow(image_cluster, interpolation = 'none');
        plt.setp(axarr[real_index], visible = True);
        
        if (hide_axes is True):
            axarr[real_index].xaxis.set_ticklabels([]);
            axarr[real_index].yaxis.set_ticklabels([]);
            
            axarr[real_index].xaxis.set_ticks_position('none');
            axarr[real_index].yaxis.set_ticks_position('none');
        
        if (double_indexer is True):
            real_index = real_index[0], real_index[1] + 1;
            if (real_index[1] >= number_cols):
                real_index = real_index[0] + 1, 0; 
        else:
            real_index += 1;

            
    plt.show();