def c6h6(df):
    """
    Calculs réglementaires pour le benzène

    Paramètres:
    df: DataFrame contenant les mesures, avec un index temporel
    (voir xair.get_mesure)

    Retourne:
    Une série de résultats dans un DataFrame :
    ******
    unité (u): µg/m3 (microgramme par mètre cube)

    Objectif de qualité en moyenne A: 2u
    Valeur limite pour la santé humaine en moyenne A: 5u

    Les résultats sont donnés en terme d'heure de dépassement

    """

    polluant = 'C6H6'

    # Le DataFrame doit être en heure
    if not isinstance(df.index.freq, pdoffset.Hour):
        raise FreqException("df doit être en heure.")

    res = {"Objectif de qualité en moyenne A: 2u": depassement(df.resample('A', how='mean'), valeur=2),
           "Valeur limite pour la santé humaine en moyenne A: 5u": depassement(df.resample('A', how='mean'), valeur=5),
           }

    return polluant, res