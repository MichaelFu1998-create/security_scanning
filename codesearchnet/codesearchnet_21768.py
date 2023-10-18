def df_quantile(df, nb=100):
    """Returns the nb quantiles for datas in a dataframe
    """
    quantiles = np.linspace(0, 1., nb)
    res = pd.DataFrame()
    for q in quantiles:
        res = res.append(df.quantile(q), ignore_index=True)
    return res