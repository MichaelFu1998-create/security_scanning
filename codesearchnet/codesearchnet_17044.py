def plot_summary_axes(graph: BELGraph, lax, rax, logx=True):
    """Plots your graph summary statistics on the given axes.

    After, you should run :func:`plt.tight_layout` and you must run :func:`plt.show` to view.

    Shows:
    1. Count of nodes, grouped by function type
    2. Count of edges, grouped by relation type

    :param pybel.BELGraph graph: A BEL graph
    :param lax: An axis object from matplotlib
    :param rax: An axis object from matplotlib

    Example usage:

    >>> import matplotlib.pyplot as plt
    >>> from pybel import from_pickle
    >>> from pybel_tools.summary import plot_summary_axes
    >>> graph = from_pickle('~/dev/bms/aetionomy/parkinsons.gpickle')
    >>> fig, axes = plt.subplots(1, 2, figsize=(10, 4))
    >>> plot_summary_axes(graph, axes[0], axes[1])
    >>> plt.tight_layout()
    >>> plt.show()
    """
    ntc = count_functions(graph)
    etc = count_relations(graph)

    df = pd.DataFrame.from_dict(dict(ntc), orient='index')
    df_ec = pd.DataFrame.from_dict(dict(etc), orient='index')

    df.sort_values(0, ascending=True).plot(kind='barh', logx=logx, ax=lax)
    lax.set_title('Number of nodes: {}'.format(graph.number_of_nodes()))

    df_ec.sort_values(0, ascending=True).plot(kind='barh', logx=logx, ax=rax)
    rax.set_title('Number of edges: {}'.format(graph.number_of_edges()))