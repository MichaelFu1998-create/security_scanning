def nombre_depassement(df, valeur, freq=None):
    """
    Calcule le nombre de d�passement d'une valeur sur l'int�gralit� du temps,
    ou suivant un regroupement temporel.

    Param�tres:
    df: DataFrame de mesures sur lequel appliqu� le calcul
    valeur: (float) valeur � chercher le d�passement (strictement sup�rieur �)
    freq: (str ou None): Fr�quence de temps sur lequel effectu� un regroupement.
    freq peut prendre les valeurs 'H' pour heure, 'D' pour jour, 'W' pour semaine,
    'M' pour mois et 'A' pour ann�e, ou None pour ne pas faire de regroupement.
    Le nombre de d�passement sera alors regroup� suivant cette fr�quence de temps.

    Retourne:
    Une Series du nombre de d�passement, total suivant la fr�quence intrins�que
    du DataFrame d'entr�e, ou agglom�r� suivant la fr�quence de temps choisie.
    """

    dep = depassement(df, valeur)
    if freq is not None:
        dep = dep.resample(freq, how='sum')
    return dep.count()