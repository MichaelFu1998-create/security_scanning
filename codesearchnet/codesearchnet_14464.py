def plot_3(data, ss, *args):
    """t-SNE embedding of the parameters, colored by score
    """

    if len(data) <= 1:
        warnings.warn("Only one datapoint. Could not compute t-SNE embedding.")
        return None

    scores = np.array([d['mean_test_score'] for d in data])
    # maps each parameters to a vector of floats
    warped = np.array([ss.point_to_unit(d['parameters']) for d in data])

    # Embed into 2 dimensions with t-SNE
    X = TSNE(n_components=2).fit_transform(warped)

    e_scores = np.exp(scores)
    mine, maxe = np.min(e_scores), np.max(e_scores)
    color = (e_scores - mine) / (maxe - mine)
    mapped_colors = list(map(rgb2hex, cm.get_cmap('RdBu_r')(color)))

    p = bk.figure(title='t-SNE (unsupervised)', tools=TOOLS)

    df_params = nonconstant_parameters(data)
    df_params['score'] = scores
    df_params['x'] = X[:, 0]
    df_params['y'] = X[:, 1]
    df_params['color'] = mapped_colors
    df_params['radius'] = 1
    p.circle(
        x='x', y='y', color='color', radius='radius',
        source=ColumnDataSource(data=df_params), fill_alpha=0.6,
        line_color=None)
    cp = p
    hover = cp.select(dict(type=HoverTool))
    format_tt = [(s, '@%s' % s) for s in df_params.columns]
    hover.tooltips = OrderedDict([("index", "$index")] + format_tt)

    xax, yax = p.axis
    xax.axis_label = 't-SNE coord 1'
    yax.axis_label = 't-SNE coord 2'
    return p