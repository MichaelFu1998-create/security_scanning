def read_graph(filename):
    """!
    @brief Read graph from file in GRPR format.
    
    @param[in] filename (string): Path to file with graph in GRPR format.
    
    @return (graph) Graph that is read from file.
    
    """
    
    file = open(filename, 'r');
    
    comments = "";
    space_descr = [];
    data = [];
    data_type = None;
    
    map_data_repr = dict();   # Used as a temporary buffer only when input graph is represented by edges.
    
    for line in file:
        if (line[0] == 'c' or line[0] == 'p'): 
            comments += line[1:]; 
        
        elif (line[0] == 'r'): 
            node_coordinates = [float(val) for val in line[1:].split()];
            if (len(node_coordinates) != 2):
                raise NameError('Invalid format of space description for node (only 2-dimension space is supported)');
                
            space_descr.append( [float(val) for val in line[1:].split()] );
        
        elif (line[0] == 'm'):
            if ( (data_type is not None) and (data_type != 'm') ):
                raise NameError('Invalid format of graph representation (only one type should be used)');
 
            data_type = 'm';
            data.append( [float(val) for val in line[1:].split()] );
        
        elif (line[0] == 'v'):
            if ( (data_type is not None) and (data_type != 'v') ):
                raise NameError('Invalid format of graph representation (only one type should be used)');
            
            data_type = 'v';
            data.append( [float(val) for val in line[1:].split()] );
            
        elif (line[0] == 'e'):
            if ( (data_type is not None) and (data_type != 'e') ):
                raise NameError('Invalid format of graph representation (only one type should be used)');
               
            data_type = 'e';
            vertices = [int(val) for val in line[1:].split()];
            
            if (vertices[0] not in map_data_repr):
                map_data_repr[ vertices[0] ] = [ vertices[1] ];
            else:
                map_data_repr[ vertices[0] ].append(vertices[1])
                
            if (vertices[1] not in map_data_repr):
                map_data_repr[ vertices[1] ] = [ vertices[0] ];
            else:
                map_data_repr[ vertices[1] ].append(vertices[0]);
            
            
        elif (len(line.strip()) == 0): continue;
        
        else: 
            print(line);
            raise NameError('Invalid format of file with graph description');
    
    # In case of edge representation result should be copied.
    if (data_type == 'e'):
        for index in range(len(map_data_repr)):
            data.append([0] * len(map_data_repr));
            
            for index_neighbour in map_data_repr[index + 1]:
                data[index][index_neighbour - 1] = 1;
    
    file.close();
    
    # Set graph description
    graph_descr = None;
    if (data_type == 'm'): graph_descr = type_graph_descr.GRAPH_MATRIX_DESCR;
    elif (data_type == 'v'): graph_descr = type_graph_descr.GRAPH_VECTOR_DESCR;
    elif (data_type == 'e'): graph_descr = type_graph_descr.GRAPH_MATRIX_DESCR;
    else:
        raise NameError('Invalid format of file with graph description');
    
    if (space_descr != []):
        if (len(data) != len(space_descr)):
            raise NameError("Invalid format of file with graph - number of nodes is different in space representation and graph description");
    
    return graph(data, graph_descr, space_descr, comments);