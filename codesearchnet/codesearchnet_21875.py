def o3(df):
    """
    Calculs r�glementaires pour l'ozone

    Param�tres:
    df: DataFrame contenant les mesures, avec un index temporel
    (voir xair.get_mesure)

    Retourne:
    Une s�rie de r�sultats dans un DataFrame :
    ******
    unit� (u): �g/m3 (microgramme par m�tre cube)

    Seuil de RI sur 1H: 180u
    Seuil d'Alerte sur 1H: 240u
    Seuil d'Alerte sur 3H cons�cutives: 240u
    Seuil d'Alerte sur 3H cons�cutives: 300u
    Seuil d'Alerte sur 1H: 360u
    Objectif de qualit� pour la sant� humaine sur 8H glissantes: 120u

    Les r�sultats sont donn�s en terme d'heure de d�passement

    """

    polluant = 'O3'

    # Le DataFrame doit �tre en heure
    if not isinstance(df.index.freq, pdoffset.Hour):
        raise FreqException("df doit �tre en heure.")

    res = {"Seuil de RI sur 1H: 180u": depassement(df, valeur=180),
           "Seuil d'Alerte sur 1H: 240u": depassement(df, valeur=240),
           "Seuil d'Alerte sur 1H: 360u": depassement(df, valeur=360),
           "Seuil d'Alerte sur 3H cons�cutives: 240u": consecutive(df, valeur=240, sur=3),
           "Seuil d'Alerte sur 3H cons�cutives: 300u": consecutive(df, valeur=300, sur=3),
           "Objectif de qualit� pour la sant� humaine sur 8H glissantes: 120u": depassement(
               moyennes_glissantes(df, sur=8), valeur=120),
           }

    return polluant, res