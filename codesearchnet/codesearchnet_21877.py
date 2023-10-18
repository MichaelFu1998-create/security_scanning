def arsenic(df):
    """
    Calculs réglementaires pour l'arsenic

    Paramètres:
    df: DataFrame contenant les mesures, avec un index temporel
    (voir xair.get_mesure)

    Retourne:
    Une série de résultats dans un DataFrame :
    ******
    unité (u): ng/m3 (nanogramme par mètre cube)

    Valeur cible en moyenne A: 6u

    Les résultats sont donnés en terme d'heure de dépassement

    """

    polluant = 'As'
    # Le DataFrame doit être en heure
    if not isinstance(df.index.freq, pdoffset.Hour):
        raise FreqException("df doit être en heure.")

    res = {"Valeur cible en moyenne A: 6u": depassement(df.resample('A', how='mean'), valeur=6),
           }

    return polluant, res