def _prepare_graph(g, g_colors, q_cls, q_arg, adjust_graph):
    """Prepares a graph for use in :class:`.QueueNetwork`.

    This function is called by ``__init__`` in the
    :class:`.QueueNetwork` class. It creates the :class:`.QueueServer`
    instances that sit on the edges, and sets various edge and node
    properties that are used when drawing the graph.

    Parameters
    ----------
    g : :any:`networkx.DiGraph`, :class:`numpy.ndarray`, dict, \
        ``None``,  etc.
        Any object that networkx can turn into a
        :any:`DiGraph<networkx.DiGraph>`
    g_colors : dict
        A dictionary of colors. The specific keys used are
        ``vertex_color`` and ``vertex_fill_color`` for vertices that
        do not have any loops. Set :class:`.QueueNetwork` for the
        default values passed.
    q_cls : dict
        A dictionary where the keys are integers that represent an edge
        type, and the values are :class:`.QueueServer` classes.
    q_args : dict
        A dictionary where the keys are integers that represent an edge
        type, and the values are the arguments that are used when
        creating an instance of that :class:`.QueueServer` class.
    adjust_graph : bool
        Specifies whether the graph will be adjusted using
        :func:`.adjacency2graph`.

    Returns
    -------
    g : :class:`.QueueNetworkDiGraph`
    queues : list
        A list of :class:`QueueServers<.QueueServer>` where
        ``queues[k]`` is the ``QueueServer`` that sets on the edge with
        edge index ``k``.

    Notes
    -----
    The graph ``g`` should have the ``edge_type`` edge property map.
    If it does not then an ``edge_type`` edge property is
    created and set to 1.

    The following properties are set by each queue: ``vertex_color``,
    ``vertex_fill_color``, ``vertex_fill_color``, ``edge_color``.
    See :class:`.QueueServer` for more on setting these values.

    The following properties are assigned as a properties to the graph;
    their default values for each edge or vertex is shown:

        * ``vertex_pen_width``: ``1``,
        * ``vertex_size``: ``8``,
        * ``edge_control_points``: ``[]``
        * ``edge_marker_size``: ``8``
        * ``edge_pen_width``: ``1.25``

    Raises
    ------
    TypeError
        Raised when the parameter ``g`` is not of a type that can be
        made into a :any:`networkx.DiGraph`.
    """
    g = _test_graph(g)

    if adjust_graph:
        pos = nx.get_node_attributes(g, 'pos')
        ans = nx.to_dict_of_dicts(g)
        g = adjacency2graph(ans, adjust=2, is_directed=g.is_directed())
        g = QueueNetworkDiGraph(g)
        if len(pos) > 0:
            g.set_pos(pos)

    g.new_vertex_property('vertex_color')
    g.new_vertex_property('vertex_fill_color')
    g.new_vertex_property('vertex_pen_width')
    g.new_vertex_property('vertex_size')

    g.new_edge_property('edge_control_points')
    g.new_edge_property('edge_color')
    g.new_edge_property('edge_marker_size')
    g.new_edge_property('edge_pen_width')

    queues = _set_queues(g, q_cls, q_arg, 'cap' in g.vertex_properties())

    if 'pos' not in g.vertex_properties():
        g.set_pos()

    for k, e in enumerate(g.edges()):
        g.set_ep(e, 'edge_pen_width', 1.25)
        g.set_ep(e, 'edge_marker_size', 8)
        if e[0] == e[1]:
            g.set_ep(e, 'edge_color', queues[k].colors['edge_loop_color'])
        else:
            g.set_ep(e, 'edge_color', queues[k].colors['edge_color'])

    for v in g.nodes():
        g.set_vp(v, 'vertex_pen_width', 1)
        g.set_vp(v, 'vertex_size', 8)
        e = (v, v)
        if g.is_edge(e):
            g.set_vp(v, 'vertex_color', queues[g.edge_index[e]]._current_color(2))
            g.set_vp(v, 'vertex_fill_color', queues[g.edge_index[e]]._current_color())
        else:
            g.set_vp(v, 'vertex_color', g_colors['vertex_color'])
            g.set_vp(v, 'vertex_fill_color', g_colors['vertex_fill_color'])

    return g, queues