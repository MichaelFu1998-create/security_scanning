def moyennes_glissantes(df, sur=8, rep=0.75):
    """
    Calcule de moyennes glissantes

    Param�tres:
    df: DataFrame de mesures sur lequel appliqu� le calcul
    sur: (int, par d�faut 8) Nombre d'observations sur lequel s'appuiera le
    calcul
    rep: (float, d�faut 0.75) Taux de r�pr�sentativit� en dessous duquel le
    calcul renverra NaN

    Retourne:
    Un DataFrame des moyennes glissantes calcul�es
    """
    return pd.rolling_mean(df, window=sur, min_periods=rep * sur)