def no2(df):
    """
    Calculs réglementaires pour le dioxyde d'azote

    Paramètres:
    df: DataFrame contenant les mesures, avec un index temporel
    (voir xair.get_mesure)

    Retourne:
    Une série de résultats dans un DataFrame :
    ******
    unité (u): µg/m3 (microgramme par mètre cube)

    Seuil de RI en moyenne H: 200u
    Seuil d'Alerte sur 3H consécutives: 400u
    Seuil d'Alerte sur 3J consécutifs: 200u
    Valeur limite pour la santé humaine 18H/A: 200u
    Valeur limite pour la santé humaine en moyenne A: 40u
    Objectif de qualité en moyenne A: 40u
    Protection de la végétation en moyenne A: 30u

    Les résultats sont donnés en terme d'heure de dépassement

    """

    polluant = "NO2"

    # Le DataFrame doit être en heure
    if not isinstance(df.index.freq, pdoffset.Hour):
        raise FreqException("df doit être en heure.")

    res = {"Seuil de RI en moyenne H: 200u": depassement(df, valeur=200),
           "Seuil d'Alerte sur 3H consécutives: 400u": consecutive(df, valeur=400, sur=3),
           "Seuil d'Alerte sur 3J consécutifs: 200u": consecutive(df.resample('D', how='max'), valeur=200, sur=3),
           "Valeur limite pour la santé humaine 18H/A: 200u": depassement(df, valeur=200),
           "Valeur limite pour la santé humaine en moyenne A: 40u": depassement(df.resample('A', how='mean'),
                                                                                 valeur=40),
           "Objectif de qualité en moyenne A: 40u": depassement(df.resample('A', how='mean'), valeur=40),
           "Protection de la végétation en moyenne A: 30u": depassement(df.resample('A', how='mean'), valeur=30),
           }

    return polluant, res