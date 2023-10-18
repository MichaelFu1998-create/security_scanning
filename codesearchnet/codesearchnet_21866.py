def moyennes_glissantes(df, sur=8, rep=0.75):
    """
    Calcule de moyennes glissantes

    Paramètres:
    df: DataFrame de mesures sur lequel appliqué le calcul
    sur: (int, par défaut 8) Nombre d'observations sur lequel s'appuiera le
    calcul
    rep: (float, défaut 0.75) Taux de réprésentativité en dessous duquel le
    calcul renverra NaN

    Retourne:
    Un DataFrame des moyennes glissantes calculées
    """
    return pd.rolling_mean(df, window=sur, min_periods=rep * sur)