def no2(df):
    """
    Calculs r�glementaires pour le dioxyde d'azote

    Param�tres:
    df: DataFrame contenant les mesures, avec un index temporel
    (voir xair.get_mesure)

    Retourne:
    Une s�rie de r�sultats dans un DataFrame :
    ******
    unit� (u): �g/m3 (microgramme par m�tre cube)

    Seuil de RI en moyenne H: 200u
    Seuil d'Alerte sur 3H cons�cutives: 400u
    Seuil d'Alerte sur 3J cons�cutifs: 200u
    Valeur limite pour la sant� humaine 18H/A: 200u
    Valeur limite pour la sant� humaine en moyenne A: 40u
    Objectif de qualit� en moyenne A: 40u
    Protection de la v�g�tation en moyenne A: 30u

    Les r�sultats sont donn�s en terme d'heure de d�passement

    """

    polluant = "NO2"

    # Le DataFrame doit �tre en heure
    if not isinstance(df.index.freq, pdoffset.Hour):
        raise FreqException("df doit �tre en heure.")

    res = {"Seuil de RI en moyenne H: 200u": depassement(df, valeur=200),
           "Seuil d'Alerte sur 3H cons�cutives: 400u": consecutive(df, valeur=400, sur=3),
           "Seuil d'Alerte sur 3J cons�cutifs: 200u": consecutive(df.resample('D', how='max'), valeur=200, sur=3),
           "Valeur limite pour la sant� humaine 18H/A: 200u": depassement(df, valeur=200),
           "Valeur limite pour la sant� humaine en moyenne A: 40u": depassement(df.resample('A', how='mean'),
                                                                                 valeur=40),
           "Objectif de qualit� en moyenne A: 40u": depassement(df.resample('A', how='mean'), valeur=40),
           "Protection de la v�g�tation en moyenne A: 30u": depassement(df.resample('A', how='mean'), valeur=30),
           }

    return polluant, res