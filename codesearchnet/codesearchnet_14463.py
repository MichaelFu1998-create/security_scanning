def plot_2(data, *args):
    """Plot 2. Running best score (scatter plot)"""
    df_all = pd.DataFrame(data)
    df_params = nonconstant_parameters(data)
    x = [df_all['id'][0]]
    y = [df_all['mean_test_score'][0]]
    params = [df_params.loc[0]]
    for i in range(len(df_all)):
        if df_all['mean_test_score'][i] > y[-1]:
            x.append(df_all['id'][i])
            y.append(df_all['mean_test_score'][i])
            params.append(df_params.loc[i])
    return build_scatter_tooltip(
        x=x, y=y, tt=pd.DataFrame(params), title='Running best')