def _diagram(plot_figure, source=None, color='black', line_color='#444444',
             xaxis_label='B-V [mag]', yaxis_label='V [mag]', name=None):
    """Use a :class:`~bokeh.plotting.figure.Figure` and x and y collections
    to create an H-R diagram.
    """
    plot_figure.circle(x='x', y='y', source=source,
                       size=5, color=color, alpha=1, name=name,
                       line_color=line_color, line_width=0.5)
    plot_figure.xaxis.axis_label = xaxis_label
    plot_figure.yaxis.axis_label = yaxis_label
    plot_figure.yaxis.formatter = NumeralTickFormatter()