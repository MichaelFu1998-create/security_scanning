def cluster_text_input(cluster, title=None):
    """
    Create an :class:`~bokeh.models.widgets.TextInput` using
    the cluster.name as the default value and title.

    If no title is provided use, 'Type in the name of your cluster
    and press Enter/Return:'.
    """
    if not title:
        title = 'Type in the name of your cluster and press Enter/Return:'
    return TextInput(value=cluster.name, title=title)