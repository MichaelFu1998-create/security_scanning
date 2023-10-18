def arsenic(df):
    """
    Calculs r�glementaires pour l'arsenic

    Param�tres:
    df: DataFrame contenant les mesures, avec un index temporel
    (voir xair.get_mesure)

    Retourne:
    Une s�rie de r�sultats dans un DataFrame :
    ******
    unit� (u): ng/m3 (nanogramme par m�tre cube)

    Valeur cible en moyenne A: 6u

    Les r�sultats sont donn�s en terme d'heure de d�passement

    """

    polluant = 'As'
    # Le DataFrame doit �tre en heure
    if not isinstance(df.index.freq, pdoffset.Hour):
        raise FreqException("df doit �tre en heure.")

    res = {"Valeur cible en moyenne A: 6u": depassement(df.resample('A', how='mean'), valeur=6),
           }

    return polluant, res