def o3(df):
    """
    Calculs réglementaires pour l'ozone

    Paramètres:
    df: DataFrame contenant les mesures, avec un index temporel
    (voir xair.get_mesure)

    Retourne:
    Une série de résultats dans un DataFrame :
    ******
    unité (u): µg/m3 (microgramme par mètre cube)

    Seuil de RI sur 1H: 180u
    Seuil d'Alerte sur 1H: 240u
    Seuil d'Alerte sur 3H consécutives: 240u
    Seuil d'Alerte sur 3H consécutives: 300u
    Seuil d'Alerte sur 1H: 360u
    Objectif de qualité pour la santé humaine sur 8H glissantes: 120u

    Les résultats sont donnés en terme d'heure de dépassement

    """

    polluant = 'O3'

    # Le DataFrame doit être en heure
    if not isinstance(df.index.freq, pdoffset.Hour):
        raise FreqException("df doit être en heure.")

    res = {"Seuil de RI sur 1H: 180u": depassement(df, valeur=180),
           "Seuil d'Alerte sur 1H: 240u": depassement(df, valeur=240),
           "Seuil d'Alerte sur 1H: 360u": depassement(df, valeur=360),
           "Seuil d'Alerte sur 3H consécutives: 240u": consecutive(df, valeur=240, sur=3),
           "Seuil d'Alerte sur 3H consécutives: 300u": consecutive(df, valeur=300, sur=3),
           "Objectif de qualité pour la santé humaine sur 8H glissantes: 120u": depassement(
               moyennes_glissantes(df, sur=8), valeur=120),
           }

    return polluant, res