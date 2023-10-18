def show_max(df):
    """Pour chaque serie (colonne) d'un DataFrame, va rechercher la (les) valeur(s)
    et la (les) date(s) du (des) max.

    Paramètres:
    df: DataFrame de valeurs à calculer

    Retourne:
    Un DataFrame montrant pour chaque serie (colonne), les valeurs maxs aux dates
    d'apparition.
    """
    df = df.astype(pd.np.float)
    res = list()
    for c in df.columns:
        serie = df[c]
        res.append(serie.where(cond=serie == serie.max(), other=pd.np.nan).dropna())
    return pd.DataFrame(res).T