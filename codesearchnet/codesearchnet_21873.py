def so2(df):
    """
    Calculs r�glementaires pour le dioxyde de soufre

    Param�tres:
    df: DataFrame contenant les mesures, avec un index temporel
    (voir xair.get_mesure)

    Retourne:
    Une s�rie de r�sultats dans un DataFrame :
    ******
    unit� (u): �g/m3 (microgramme par m�tre cube)

    Seuil de RI en moyenne H: 300u
    Seuil d'Alerte sur 3H cons�cutives: 500u
    Valeur limite pour la sant� humaine 24H/A: 350u
    Valeur limite pour la sant� humaine 3J/A: 125u
    Objectif de qualit� en moyenne A: 50u
    Protection de la v�g�tation en moyenne A: 20u
    Protection de la v�g�tation du 01/10 au 31/03: 20u

    Les r�sultats sont donn�s en terme d'heure de d�passement

    """

    polluant = 'SO2'

    # Le DataFrame doit �tre en heure
    if not isinstance(df.index.freq, pdoffset.Hour):
        raise FreqException("df doit �tre en heure.")

    res = {"Seuil de RI en moyenne H: 300u": depassement(df, valeur=300),
           "Seuil d'Alerte sur 3H cons�cutives: 500u": depassement(df, valeur=500),
           "Valeur limite pour la sant� humaine 24H/A: 350u": depassement(df, valeur=350),
           "Valeur limite pour la sant� humaine 3J/A: 125u": depassement(df.resample('D', how='mean'), valeur=125),
           "Objectif de qualit� en moyenne A: 50u": depassement(df.resample('A', how='mean'), valeur=50),
           "Protection de la v�g�tation en moyenne A: 20u": depassement(df.resample('A', how='mean'), valeur=20),
           "Protection de la v�g�tation du 01/10 au 31/03: 20u": depassement(
               df[(df.index.month <= 3) | (df.index.month >= 10)], valeur=20),
           }

    return polluant, res