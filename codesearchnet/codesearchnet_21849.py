def profil_hebdo(df, func='mean'):
    """
    Calcul du profil journalier

    Param�tres:
    df: DataFrame de donn�es dont l'index est une s�rie temporelle
        (cf module xair par exemple)
    func: function permettant le calcul. Soit un nom de fonction numpy ('mean', 'max', ...)
        soit la fonction elle-m�me (np.mean, np.max, ...)
    Retourne:
    Un DataFrame de moyennes par journ�e sur la semaine
    """

    func = _get_funky(func)
    res = df.groupby(lambda x: x.weekday).aggregate(func)
    # On met des noms de jour � la place des num�ros dans l'index
    res.index = [cal.day_name[i] for i in range(0,7)]
    return res