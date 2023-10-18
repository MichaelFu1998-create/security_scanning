def co(df):
    """
    Calculs r�glementaires pour le monoxyde de carbone

    Param�tres:
    df: DataFrame contenant les mesures, avec un index temporel
    (voir xair.get_mesure)

    Retourne:
    Une s�rie de r�sultats dans un DataFrame :
    ******
    unit� (u): �g/m3 (microgramme par m�tre cube)

    Valeur limite pour la sant� humaine max J 8H glissantes: 10000u

    Les r�sultats sont donn�s en terme d'heure de d�passement

    """

    polluant = 'CO'

    # Le DataFrame doit �tre en heure
    if not isinstance(df.index.freq, pdoffset.Hour):
        raise FreqException("df doit �tre en heure.")

    res = {"Valeur limite pour la sant� humaine sur 8H glissantes: 10000u": depassement(moyennes_glissantes(df, sur=8),
                                                                                         valeur=10),
           }

    return polluant, res