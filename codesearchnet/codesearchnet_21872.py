def pm10(df):
    """
    Calculs r�glementaires pour les particules PM10

    Param�tres:
    df: DataFrame contenant les mesures, avec un index temporel
    (voir xair.get_mesure)

    Retourne:
    Une s�rie de r�sultats dans un DataFrame :
    ******
    unit� (u): �g/m3 (microgramme par m�tre cube)

    Seuil de RI en moyenne J: 50u
    Seuil d'Alerte en moyenne J: 80u
    Valeur limite pour la sant� humaine 35J/A: 50u
    Valeur limite pour la sant� humaine en moyenne A: 40u
    Objectif de qualit� en moyenne A: 30u

    Les r�sultats sont donn�s en terme d'heure de d�passement

    """

    polluant = 'PM10'
    # Le DataFrame doit �tre en jour
    if not isinstance(df.index.freq, pdoffset.Day):
        raise FreqException("df doit �tre en jour.")

    res = {"Seuil de RI en moyenne J: 50u": depassement(df, valeur=50),
           "Seuil d'Alerte en moyenne J: 80u": depassement(df, valeur=80),
           "Valeur limite pour la sant� humaine 35J/A: 50u": depassement(df, valeur=50),
           "Valeur limite pour la sant� humaine en moyenne A: 40u": depassement(df.resample('A', how='mean'),
                                                                                 valeur=40),
           "Objectif de qualit� en moyenne A: 30u": depassement(df.resample('A', how='mean'), valeur=30),
           }

    return polluant, res