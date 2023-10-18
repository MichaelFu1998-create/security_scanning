def to_date(date, dayfirst=False, format=None):
    """
    Transforme un champ date vers un objet python datetime
    Paramètres:
    date:
        - si None, renvoie la date du jour
        - si de type str, renvoie un objet python datetime
        - si de type datetime, le retourne sans modification
    dayfirst: Si True, aide l'analyse du champ date de type str en informant
    le décrypteur que le jour se situe en début de chaîne (ex:11/09/2012
    pourrait être interpreté comme le 09 novembre si dayfirst=False)
    format: chaîne de caractère décrivant précisement le champ date de type
    str. Voir la documentation officielle de python.datetime pour description

    """
    ## TODO: voir si pd.tseries.api ne peut pas remplacer tout ca
    if not date:
        return dt.datetime.fromordinal(
            dt.date.today().toordinal())  # mieux que dt.datetime.now() car ca met les heures, minutes et secondes à zéro
    elif isinstance(date, dt.datetime):
        return date
    elif isinstance(date, str):
        return pd.to_datetime(date, dayfirst=dayfirst, format=format)
    elif isinstance(date, dt.date):
        return dt.datetime.fromordinal(date.toordinal())
    else:
        raise ValueError("Les dates doivent être de type None, str, datetime.date ou datetime.datetime")