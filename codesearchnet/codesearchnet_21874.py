def co(df):
    """
    Calculs réglementaires pour le monoxyde de carbone

    Paramètres:
    df: DataFrame contenant les mesures, avec un index temporel
    (voir xair.get_mesure)

    Retourne:
    Une série de résultats dans un DataFrame :
    ******
    unité (u): µg/m3 (microgramme par mètre cube)

    Valeur limite pour la santé humaine max J 8H glissantes: 10000u

    Les résultats sont donnés en terme d'heure de dépassement

    """

    polluant = 'CO'

    # Le DataFrame doit être en heure
    if not isinstance(df.index.freq, pdoffset.Hour):
        raise FreqException("df doit être en heure.")

    res = {"Valeur limite pour la santé humaine sur 8H glissantes: 10000u": depassement(moyennes_glissantes(df, sur=8),
                                                                                         valeur=10),
           }

    return polluant, res