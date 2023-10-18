def plot_1(data, *args):
    """Plot 1. All iterations (scatter plot)"""
    df_all = pd.DataFrame(data)
    df_params = nonconstant_parameters(data)
    return build_scatter_tooltip(
        x=df_all['id'], y=df_all['mean_test_score'], tt=df_params,
        title='All Iterations')