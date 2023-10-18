def profil_hebdo(df, func='mean'):
    """
    Calcul du profil journalier

    Paramètres:
    df: DataFrame de données dont l'index est une série temporelle
        (cf module xair par exemple)
    func: function permettant le calcul. Soit un nom de fonction numpy ('mean', 'max', ...)
        soit la fonction elle-même (np.mean, np.max, ...)
    Retourne:
    Un DataFrame de moyennes par journée sur la semaine
    """

    func = _get_funky(func)
    res = df.groupby(lambda x: x.weekday).aggregate(func)
    # On met des noms de jour à la place des numéros dans l'index
    res.index = [cal.day_name[i] for i in range(0,7)]
    return res