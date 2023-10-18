def profil_annuel(df, func='mean'):
    """
    Calcul du profil annuel

    Paramètres:
    df: DataFrame de données dont l'index est une série temporelle
        (cf module xair par exemple)
    func: function permettant le calcul. Soit un nom de fonction numpy ('mean', 'max', ...)
        soit la fonction elle-même (np.mean, np.max, ...)
    Retourne:
    Un DataFrame de moyennes par mois
    """

    func = _get_funky(func)
    res = df.groupby(lambda x: x.month).aggregate(func)
    # On met des noms de mois à la place des numéros dans l'index
    res.index = [cal.month_name[i] for i in range(1,13)]
    return res