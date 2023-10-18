def nombre_depassement(df, valeur, freq=None):
    """
    Calcule le nombre de dépassement d'une valeur sur l'intégralité du temps,
    ou suivant un regroupement temporel.

    Paramètres:
    df: DataFrame de mesures sur lequel appliqué le calcul
    valeur: (float) valeur à chercher le dépassement (strictement supérieur à)
    freq: (str ou None): Fréquence de temps sur lequel effectué un regroupement.
    freq peut prendre les valeurs 'H' pour heure, 'D' pour jour, 'W' pour semaine,
    'M' pour mois et 'A' pour année, ou None pour ne pas faire de regroupement.
    Le nombre de dépassement sera alors regroupé suivant cette fréquence de temps.

    Retourne:
    Une Series du nombre de dépassement, total suivant la fréquence intrinsèque
    du DataFrame d'entrée, ou aggloméré suivant la fréquence de temps choisie.
    """

    dep = depassement(df, valeur)
    if freq is not None:
        dep = dep.resample(freq, how='sum')
    return dep.count()