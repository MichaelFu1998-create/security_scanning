def plot_summary(graph: BELGraph, plt, logx=True, **kwargs):
    """Plots your graph summary statistics. This function is a thin wrapper around :func:`plot_summary_axis`. It
    automatically takes care of building figures given matplotlib's pyplot module as an argument. After, you need
    to run :func:`plt.show`.

    :code:`plt` is given as an argument to avoid needing matplotlib as a dependency for this function

    Shows:

    1. Count of nodes, grouped by function type
    2. Count of edges, grouped by relation type

    :param plt: Give :code:`matplotlib.pyplot` to this parameter
    :param kwargs: keyword arguments to give to :func:`plt.subplots`

    Example usage:

    >>> import matplotlib.pyplot as plt
    >>> from pybel import from_pickle
    >>> from pybel_tools.summary import plot_summary
    >>> graph = from_pickle('~/dev/bms/aetionomy/parkinsons.gpickle')
    >>> plot_summary(graph, plt, figsize=(10, 4))
    >>> plt.show()
    """
    fig, axes = plt.subplots(1, 2, **kwargs)
    lax = axes[0]
    rax = axes[1]

    plot_summary_axes(graph, lax, rax, logx=logx)
    plt.tight_layout()

    return fig, axes