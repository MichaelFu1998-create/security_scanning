def pm10(df):
    """
    Calculs réglementaires pour les particules PM10

    Paramètres:
    df: DataFrame contenant les mesures, avec un index temporel
    (voir xair.get_mesure)

    Retourne:
    Une série de résultats dans un DataFrame :
    ******
    unité (u): µg/m3 (microgramme par mètre cube)

    Seuil de RI en moyenne J: 50u
    Seuil d'Alerte en moyenne J: 80u
    Valeur limite pour la santé humaine 35J/A: 50u
    Valeur limite pour la santé humaine en moyenne A: 40u
    Objectif de qualité en moyenne A: 30u

    Les résultats sont donnés en terme d'heure de dépassement

    """

    polluant = 'PM10'
    # Le DataFrame doit être en jour
    if not isinstance(df.index.freq, pdoffset.Day):
        raise FreqException("df doit être en jour.")

    res = {"Seuil de RI en moyenne J: 50u": depassement(df, valeur=50),
           "Seuil d'Alerte en moyenne J: 80u": depassement(df, valeur=80),
           "Valeur limite pour la santé humaine 35J/A: 50u": depassement(df, valeur=50),
           "Valeur limite pour la santé humaine en moyenne A: 40u": depassement(df.resample('A', how='mean'),
                                                                                 valeur=40),
           "Objectif de qualité en moyenne A: 30u": depassement(df.resample('A', how='mean'), valeur=30),
           }

    return polluant, res