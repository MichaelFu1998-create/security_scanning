def consecutive(df, valeur, sur=3):
    """Calcule si une valeur est d�pass�e durant une p�riode donn�e. D�tecte
    un d�passement de valeur sur X heures/jours/... cons�cutifs

    Param�tres:
    df: DataFrame de mesures sur lequel appliqu� le calcul
    valeur: (float) valeur � chercher le d�passement (strictement sup�rieur �)
    sur: (int) Nombre d'observations cons�cutives o� la valeur doit �tre d�pass�e

    Retourne:
    Un DataFrame de valeurs, de m�me taille (shape) que le df d'entr�e, dont toutes
    les valeurs sont supprim�es, sauf celles sup�rieures � la valeur de r�f�rence
    et positionn�es sur les heures de d�but de d�passements

    """

    dep = pd.rolling_max(df.where(df > valeur), window=sur, min_periods=sur)
    return dep