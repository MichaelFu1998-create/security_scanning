def aot40_vegetation(df, nb_an):
    """
    Calcul de l'AOT40 du 1er mai au 31 juillet

    *AOT40 : AOT 40 ( exprimé en micro g/m³ par heure ) signifie la somme des
    différences entre les concentrations horaires supérieures à 40 parties par
    milliard ( 40 ppb soit 80 micro g/m³ ), durant une période donnée en
    utilisant uniquement les valeurs sur 1 heure mesurées quotidiennement
    entre 8 heures (début de la mesure) et 20 heures (pile, fin de la mesure) CET,
    ce qui correspond à de 8h à 19h TU (donnant bien 12h de mesures, 8h donnant
    la moyenne horaire de 7h01 à 8h00)

    Paramètres:
    df: DataFrame de mesures sur lequel appliqué le calcul
    nb_an: (int) Nombre d'années contenu dans le df, et servant à diviser le
    résultat retourné

    Retourne:
    Un DataFrame de résultat de calcul
    """

    return _aot(df.tshift(1), nb_an=nb_an, limite=80, mois_debut=5, mois_fin=7,
                heure_debut=8, heure_fin=19)