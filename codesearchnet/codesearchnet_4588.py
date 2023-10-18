def draw_image_color_segments(source, clusters, hide_axes = True):
    """!
    @brief Shows image segments using colored image.
    @details Each color on result image represents allocated segment. The first image is initial and other is result of segmentation.
    
    @param[in] source (string): Path to image.
    @param[in] clusters (list): List of clusters (allocated segments of image) where each cluster
                                consists of indexes of pixel from source image.
    @param[in] hide_axes (bool): If True then axes will not be displayed.
    
    """
        
    image_source = Image.open(source);
    image_size = image_source.size;
    
    (fig, axarr) = plt.subplots(1, 2);
    
    plt.setp([ax for ax in axarr], visible = False);
    
    available_colors = [ (0, 162, 232),   (34, 177, 76),   (237, 28, 36),
                         (255, 242, 0),   (0, 0, 0),       (237, 28, 36),
                         (255, 174, 201), (127, 127, 127), (185, 122, 87), 
                         (200, 191, 231), (136, 0, 21),    (255, 127, 39),
                         (63, 72, 204),   (195, 195, 195), (255, 201, 14),
                         (239, 228, 176), (181, 230, 29),  (153, 217, 234),
                         (112, 146, 180) ];
    
    image_color_segments = [(255, 255, 255)] * (image_size[0] * image_size[1]);
    
    for index_segment in range(len(clusters)):
        for index_pixel in clusters[index_segment]:
            image_color_segments[index_pixel] = available_colors[index_segment];
    
    stage = array(image_color_segments, numpy.uint8);
    stage = numpy.reshape(stage, (image_size[1], image_size[0]) + ((3),)); # ((3),) it's size of RGB - third dimension.
    image_cluster = Image.fromarray(stage, 'RGB');
    
    axarr[0].imshow(image_source, interpolation = 'none');
    axarr[1].imshow(image_cluster, interpolation = 'none');
    
    for i in range(2):
        plt.setp(axarr[i], visible = True);
        
        if (hide_axes is True):
            axarr[i].xaxis.set_ticklabels([]);
            axarr[i].yaxis.set_ticklabels([]);
            axarr[i].xaxis.set_ticks_position('none');
            axarr[i].yaxis.set_ticks_position('none');
    
    plt.show();