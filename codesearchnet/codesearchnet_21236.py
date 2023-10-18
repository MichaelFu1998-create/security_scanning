def hr_diagram(cluster_name, output=None):
    """Create a :class:`~bokeh.plotting.figure.Figure` to create an H-R
    diagram using the cluster_name; then show it.

    Re
    """
    cluster = get_hr_data(cluster_name)
    pf = hr_diagram_figure(cluster)
    show_with_bokeh_server(pf)