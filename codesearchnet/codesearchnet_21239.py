def hr_diagram_figure(cluster):
    """
    Given a cluster create a Bokeh plot figure creating an
    H-R diagram.
    """
    temps, lums = round_teff_luminosity(cluster)
    x, y = temps, lums
    colors, color_mapper = hr_diagram_color_helper(temps)
    x_range = [max(x) + max(x) * 0.05, min(x) - min(x) * 0.05]
    source = ColumnDataSource(data=dict(x=x, y=y, color=colors))

    pf = figure(y_axis_type='log', x_range=x_range, name='hr',
                tools='box_select,lasso_select,reset,hover',
                title='H-R Diagram for {0}'.format(cluster.name))
    pf.select(BoxSelectTool).select_every_mousemove = False
    pf.select(LassoSelectTool).select_every_mousemove = False
    hover = pf.select(HoverTool)[0]
    hover.tooltips = [("Temperature (Kelvin)", "@x{0}"),
                      ("Luminosity (solar units)", "@y{0.00}")]
    _diagram(source=source, plot_figure=pf, name='hr',
             color={'field': 'color', 'transform': color_mapper},
             xaxis_label='Temperature (Kelvin)',
             yaxis_label='Luminosity (solar units)')
    return pf