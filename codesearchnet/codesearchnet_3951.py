def SID(target, pred):
    """Compute the Strutural Intervention Distance.
    
    [R wrapper] The Structural Intervention Distance (SID) is a new distance
    for graphs introduced by Peters and Bühlmann (2013). This distance was
    created to account for the shortcomings of the SHD metric for a causal 
    sense.
    It consists in computing the path between all the pairs of variables, and
    checks if the causal relationship between the variables is respected.
    The given graphs have to be DAGs for the SID metric to make sense.

    Args:
        target (numpy.ndarray or networkx.DiGraph): Target graph, must be of 
            ones and zeros, and instance of either numpy.ndarray or 
            networkx.DiGraph. Must be a DAG.

        prediction (numpy.ndarray or networkx.DiGraph): Prediction made by the
            algorithm to evaluate. Must be a DAG.
 
    Returns:
        int: Structural Intervention Distance. 

            The value tends to zero as the graphs tends to be identical.
        
    .. note::
        Ref: Structural Intervention Distance (SID) for Evaluating Causal Graphs,
        Jonas Peters, Peter Bühlmann: https://arxiv.org/abs/1306.1043
    
    Examples:
        >>> from numpy.random import randint
        >>> tar = np.triu(randint(2, size=(10, 10))) 
        >>> pred = np.triu(randint(2, size=(10, 10)))
        >>> SID(tar, pred) 
   """
    if not RPackages.SID:
        raise ImportError("SID R package is not available. Please check your installation.")

    true_labels = retrieve_adjacency_matrix(target)
    predictions = retrieve_adjacency_matrix(pred, target.nodes() 
                                            if isinstance(target, nx.DiGraph) else None)
    
    os.makedirs('/tmp/cdt_SID/')

    def retrieve_result():
        return np.loadtxt('/tmp/cdt_SID/result.csv')

    try:
        np.savetxt('/tmp/cdt_SID/target.csv', true_labels, delimiter=',')
        np.savetxt('/tmp/cdt_SID/pred.csv', predictions, delimiter=',')
        sid_score = launch_R_script("{}/R_templates/sid.R".format(os.path.dirname(os.path.realpath(__file__))),
                                    {"{target}": '/tmp/cdt_SID/target.csv',
                                     "{prediction}": '/tmp/cdt_SID/pred.csv',
                                     "{result}": '/tmp/cdt_SID/result.csv'},
                                    output_function=retrieve_result)
    # Cleanup
    except Exception as e:
        rmtree('/tmp/cdt_SID')
        raise e
    except KeyboardInterrupt:
        rmtree('/tmp/cdt_SID/')
        raise KeyboardInterrupt

    rmtree('/tmp/cdt_SID')
    return sid_score