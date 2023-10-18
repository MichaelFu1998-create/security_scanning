def draw_graph(graph_instance, map_coloring = None):
    """!
    @brief Draw graph.

    @param[in] graph_instance (graph): Graph that should be drawn.
    @param[in] map_coloring (list): List of color indexes for each vertex. Size of this list should be equal to size of graph (number of vertices).
                                    If it's not specified (None) than graph without coloring will be dwarn.
    
    @warning Graph can be represented if there is space representation for it.
    
    """
    
    if (graph_instance.space_description is None):
        raise NameError("The graph haven't got representation in space");
    
    if (map_coloring is not None):
        if (len(graph_instance) != len(map_coloring)):
            raise NameError("Size of graph should be equal to size coloring map");
        
    
    fig = plt.figure();
    axes = fig.add_subplot(111);
    
    available_colors = ['#00a2e8', '#22b14c', '#ed1c24',
                        '#fff200', '#000000', '#a349a4',
                        '#ffaec9', '#7f7f7f', '#b97a57',
                        '#c8bfe7', '#880015', '#ff7f27',
                        '#3f48cc', '#c3c3c3', '#ffc90e',
                        '#efe4b0', '#b5e61d', '#99d9ea',
                        '#7092b4', '#ffffff'];
              
    if (map_coloring is not None):
        if (len(map_coloring) > len(available_colors)):
            raise NameError('Impossible to represent colored graph due to number of specified colors.');
    
    x_maximum = -float('inf');
    x_minimum = float('inf');
    y_maximum = -float('inf');
    y_minimum = float('inf');
    
    for i in range(0, len(graph_instance.space_description), 1):
        if (graph_instance.type_graph_descr == type_graph_descr.GRAPH_MATRIX_DESCR):
            for j in range(i, len(graph_instance.space_description), 1):    # draw connection between two points only one time
                if (graph_instance.data[i][j] == 1):
                    axes.plot([graph_instance.space_description[i][0], graph_instance.space_description[j][0]], [graph_instance.space_description[i][1], graph_instance.space_description[j][1]], 'k-', linewidth = 1.5);
                    
        elif (graph_instance.type_graph_descr == type_graph_descr.GRAPH_VECTOR_DESCR):
            for j in graph_instance.data[i]:
                if (i > j):     # draw connection between two points only one time
                    axes.plot([graph_instance.space_description[i][0], graph_instance.space_description[j][0]], [graph_instance.space_description[i][1], graph_instance.space_description[j][1]], 'k-', linewidth = 1.5);   
            
        color_node = 'b';
        if (map_coloring is not None):
            color_node = colors.hex2color(available_colors[map_coloring[i]]);
        
        axes.plot(graph_instance.space_description[i][0], graph_instance.space_description[i][1], color = color_node, marker = 'o', markersize = 20);
    
        if (x_maximum < graph_instance.space_description[i][0]): x_maximum = graph_instance.space_description[i][0];
        if (x_minimum > graph_instance.space_description[i][0]): x_minimum = graph_instance.space_description[i][0];  
        if (y_maximum < graph_instance.space_description[i][1]): y_maximum = graph_instance.space_description[i][1]; 
        if (y_minimum > graph_instance.space_description[i][1]): y_minimum = graph_instance.space_description[i][1];
    
    plt.xlim(x_minimum - 0.5, x_maximum + 0.5);
    plt.ylim(y_minimum - 0.5, y_maximum + 0.5);
    
    plt.show();