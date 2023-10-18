def taux_de_representativite(df):
    """Calcul le taux de repr�sentativit� d'un dataframe"""
    return (df.count().astype(pd.np.float) / df.shape[0] * 100).round(1)