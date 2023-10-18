def so2(df):
    """
    Calculs réglementaires pour le dioxyde de soufre

    Paramètres:
    df: DataFrame contenant les mesures, avec un index temporel
    (voir xair.get_mesure)

    Retourne:
    Une série de résultats dans un DataFrame :
    ******
    unité (u): µg/m3 (microgramme par mètre cube)

    Seuil de RI en moyenne H: 300u
    Seuil d'Alerte sur 3H consécutives: 500u
    Valeur limite pour la santé humaine 24H/A: 350u
    Valeur limite pour la santé humaine 3J/A: 125u
    Objectif de qualité en moyenne A: 50u
    Protection de la végétation en moyenne A: 20u
    Protection de la végétation du 01/10 au 31/03: 20u

    Les résultats sont donnés en terme d'heure de dépassement

    """

    polluant = 'SO2'

    # Le DataFrame doit être en heure
    if not isinstance(df.index.freq, pdoffset.Hour):
        raise FreqException("df doit être en heure.")

    res = {"Seuil de RI en moyenne H: 300u": depassement(df, valeur=300),
           "Seuil d'Alerte sur 3H consécutives: 500u": depassement(df, valeur=500),
           "Valeur limite pour la santé humaine 24H/A: 350u": depassement(df, valeur=350),
           "Valeur limite pour la santé humaine 3J/A: 125u": depassement(df.resample('D', how='mean'), valeur=125),
           "Objectif de qualité en moyenne A: 50u": depassement(df.resample('A', how='mean'), valeur=50),
           "Protection de la végétation en moyenne A: 20u": depassement(df.resample('A', how='mean'), valeur=20),
           "Protection de la végétation du 01/10 au 31/03: 20u": depassement(
               df[(df.index.month <= 3) | (df.index.month >= 10)], valeur=20),
           }

    return polluant, res