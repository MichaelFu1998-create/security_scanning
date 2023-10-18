def hr_diagram_from_data(data, x_range, y_range):
    """
    Given a numpy array create a Bokeh plot figure creating an
    H-R diagram.
    """
    _, color_mapper = hr_diagram_color_helper([])
    data_dict = {
        'x': list(data['temperature']),
        'y': list(data['luminosity']),
        'color': list(data['color'])
    }
    source = ColumnDataSource(data=data_dict)
    pf = figure(y_axis_type='log', x_range=x_range, y_range=y_range)
    _diagram(source=source, plot_figure=pf,
             color={'field': 'color', 'transform': color_mapper},
             xaxis_label='Temperature (Kelvin)',
             yaxis_label='Luminosity (solar units)')
    show_with_bokeh_server(pf)