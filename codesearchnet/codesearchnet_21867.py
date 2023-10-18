def consecutive(df, valeur, sur=3):
    """Calcule si une valeur est dépassée durant une période donnée. Détecte
    un dépassement de valeur sur X heures/jours/... consécutifs

    Paramètres:
    df: DataFrame de mesures sur lequel appliqué le calcul
    valeur: (float) valeur à chercher le dépassement (strictement supérieur à)
    sur: (int) Nombre d'observations consécutives où la valeur doit être dépassée

    Retourne:
    Un DataFrame de valeurs, de même taille (shape) que le df d'entrée, dont toutes
    les valeurs sont supprimées, sauf celles supérieures à la valeur de référence
    et positionnées sur les heures de début de dépassements

    """

    dep = pd.rolling_max(df.where(df > valeur), window=sur, min_periods=sur)
    return dep