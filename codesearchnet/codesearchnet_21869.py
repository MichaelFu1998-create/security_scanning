def aot40_vegetation(df, nb_an):
    """
    Calcul de l'AOT40 du 1er mai au 31 juillet

    *AOT40 : AOT 40 ( exprim� en micro g/m� par heure ) signifie la somme des
    diff�rences entre les concentrations horaires sup�rieures � 40 parties par
    milliard ( 40 ppb soit 80 micro g/m� ), durant une p�riode donn�e en
    utilisant uniquement les valeurs sur 1 heure mesur�es quotidiennement
    entre 8 heures (d�but de la mesure) et 20 heures (pile, fin de la mesure) CET,
    ce qui correspond � de 8h � 19h TU (donnant bien 12h de mesures, 8h donnant
    la moyenne horaire de 7h01 � 8h00)

    Param�tres:
    df: DataFrame de mesures sur lequel appliqu� le calcul
    nb_an: (int) Nombre d'ann�es contenu dans le df, et servant � diviser le
    r�sultat retourn�

    Retourne:
    Un DataFrame de r�sultat de calcul
    """

    return _aot(df.tshift(1), nb_an=nb_an, limite=80, mois_debut=5, mois_fin=7,
                heure_debut=8, heure_fin=19)