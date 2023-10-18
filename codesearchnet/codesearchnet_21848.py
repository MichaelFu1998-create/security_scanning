def profil_journalier(df, func='mean'):
    """
    Calcul du profil journalier

    Param�tres:
    df: DataFrame de donn�es dont l'index est une s�rie temporelle
        (cf module xair par exemple)
    func: function permettant le calcul. Soit un nom de fonction numpy ('mean', 'max', ...)
        soit la fonction elle-m�me (np.mean, np.max, ...)
    Retourne:
    Un DataFrame de moyennes par heure sur une journ�e
    """

    func = _get_funky(func)
    res = df.groupby(lambda x: x.hour).aggregate(func)
    return res