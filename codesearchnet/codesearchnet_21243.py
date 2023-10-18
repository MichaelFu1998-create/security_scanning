def hr_diagram_selection(cluster_name):
    """
    Given a cluster create two Bokeh plot based H-R diagrams.
    The Selection in the left H-R diagram will show up on the
    right one.
    """
    cluster = get_hr_data(cluster_name)
    temps, lums = round_teff_luminosity(cluster)
    x, y = temps, lums
    colors, color_mapper = hr_diagram_color_helper(temps)
    x_range = [max(x) + max(x) * 0.05, min(x) - min(x) * 0.05]
    source = ColumnDataSource(data=dict(x=x, y=y, color=colors), name='hr')
    source_selected = ColumnDataSource(data=dict(x=[], y=[], color=[]),
                                       name='hr')
    pf = figure(y_axis_type='log', x_range=x_range,
                tools='lasso_select,reset',
                title='H-R Diagram for {0}'.format(cluster.name))
    _diagram(source=source, plot_figure=pf, name='hr', color={'field':
             'color', 'transform': color_mapper},
             xaxis_label='Temperature (Kelvin)',
             yaxis_label='Luminosity (solar units)')
    pf_selected = figure(y_axis_type='log', y_range=pf.y_range,
                         x_range=x_range,
                         tools='reset',
                         title='H-R Diagram for {0}'.format(cluster.name))
    _diagram(source=source_selected, plot_figure=pf_selected, name='hr',
             color={'field': 'color', 'transform': color_mapper},
             xaxis_label='Temperature (Kelvin)',
             yaxis_label='Luminosity (solar units)')
    source.callback = CustomJS(args=dict(source_selected=source_selected),
                               code="""
        var inds = cb_obj.selected['1d'].indices;
        var d1 = cb_obj.data;
        var d2 = source_selected.data;
        console.log(inds);
        d2['x'] = []
        d2['y'] = []
        d2['color'] = []
        for (i = 0; i < inds.length; i++) {
            d2['x'].push(d1['x'][inds[i]])
            d2['y'].push(d1['y'][inds[i]])
            d2['color'].push(d1['color'][inds[i]])
        }
        source_selected.change.emit();
        """)
    show_with_bokeh_server(row(pf, pf_selected))