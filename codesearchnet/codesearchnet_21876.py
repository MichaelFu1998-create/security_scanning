def c6h6(df):
    """
    Calculs r�glementaires pour le benz�ne

    Param�tres:
    df: DataFrame contenant les mesures, avec un index temporel
    (voir xair.get_mesure)

    Retourne:
    Une s�rie de r�sultats dans un DataFrame :
    ******
    unit� (u): �g/m3 (microgramme par m�tre cube)

    Objectif de qualit� en moyenne A: 2u
    Valeur limite pour la sant� humaine en moyenne A: 5u

    Les r�sultats sont donn�s en terme d'heure de d�passement

    """

    polluant = 'C6H6'

    # Le DataFrame doit �tre en heure
    if not isinstance(df.index.freq, pdoffset.Hour):
        raise FreqException("df doit �tre en heure.")

    res = {"Objectif de qualit� en moyenne A: 2u": depassement(df.resample('A', how='mean'), valeur=2),
           "Valeur limite pour la sant� humaine en moyenne A: 5u": depassement(df.resample('A', how='mean'), valeur=5),
           }

    return polluant, res