def draw_net_using_node_coords(net):
    """
    Plot a networkx.Graph by using the lat and lon attributes of nodes.
    Parameters
    ----------
    net : networkx.Graph
    Returns
    -------
    fig : matplotlib.figure
        the figure object where the network is plotted
    """
    import matplotlib.pyplot as plt
    fig = plt.figure()
    node_coords = {}
    for node, data in net.nodes(data=True):
        node_coords[node] = (data['lon'], data['lat'])
    ax = fig.add_subplot(111)
    networkx.draw(net, pos=node_coords, ax=ax, node_size=50)
    return fig