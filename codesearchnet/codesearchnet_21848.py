def profil_journalier(df, func='mean'):
    """
    Calcul du profil journalier

    Paramètres:
    df: DataFrame de données dont l'index est une série temporelle
        (cf module xair par exemple)
    func: function permettant le calcul. Soit un nom de fonction numpy ('mean', 'max', ...)
        soit la fonction elle-même (np.mean, np.max, ...)
    Retourne:
    Un DataFrame de moyennes par heure sur une journée
    """

    func = _get_funky(func)
    res = df.groupby(lambda x: x.hour).aggregate(func)
    return res