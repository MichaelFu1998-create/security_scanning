def plot_4(data, *args):
    """Scatter plot of score vs each param
    """
    params = nonconstant_parameters(data)
    scores = np.array([d['mean_test_score'] for d in data])
    order = np.argsort(scores)

    for key in params.keys():
        if params[key].dtype == np.dtype('bool'):
            params[key] = params[key].astype(np.int)
    p_list = []
    for key in params.keys():
        x = params[key][order]
        y = scores[order]
        params = params.loc[order]
        try:
            radius = (np.max(x) - np.min(x)) / 100.0
        except:
            print("error making plot4 for '%s'" % key)
            continue

        p_list.append(build_scatter_tooltip(
            x=x, y=y, radius=radius, add_line=False, tt=params,
            xlabel=key, title='Score vs %s' % key))
    return p_list