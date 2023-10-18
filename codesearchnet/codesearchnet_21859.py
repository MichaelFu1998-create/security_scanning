def get_mesures(self, mes, debut=None, fin=None, freq='H', format=None,
                    dayfirst=False, brut=False):
        """
        Récupération des données de mesure.

        Paramètres:
        mes: Un nom de mesure ou plusieurs séparées par des virgules, une liste
            (list, tuple, pandas.Series) de noms
        debut: Chaine de caractère ou objet datetime décrivant la date de début.
            Défaut=date du jour
        fin: Chaine de caractère ou objet datetime décrivant la date de fin.
            Défaut=date de début
        freq: fréquence de temps. '15T' | 'H' | 'D' | 'M' | 'A' (15T pour quart-horaire)
        format: chaine de caractère décrivant le format des dates (ex:"%Y-%m-%d"
            pour debut/fin="2013-01-28"). Appeler pyair.date.strtime_help() pour
            obtenir la liste des codes possibles.
            Defaut="%Y-%m-%d"
        dayfirst: Si aucun format n'est fourni et que les dates sont des chaines
            de caractères, aide le décrypteur à transformer la date en objet datetime
            en spécifiant que les dates commencent par le jour (ex:11/09/2012
            pourrait être interpreté comme le 09 novembre si dayfirst=False)
        brut: si oui ou non renvoyer le dataframe brut, non invalidé, et les
            codes d'état des mesures
            Defaut=False

        Retourne:
        Un dataframe contenant toutes les mesures demandées.
        Si brut=True, renvoie le  dataframe des mesures brutes non invalidées et
        le dataframe des codes d'états.
        Le dataframe valide (net) peut être alors recalculé en faisant:
        brut, etats = xr.get_mesure(..., brut=True)
        invalides = etats_to_invalid(etats)
        net = brut.mask(invalides)

        """

        def create_index(index, freq):
            """
            Nouvel index [id, date] avec date formaté suivant le pas de temps voulu
            index: index de l'ancien dataframe, tel que [date à minuit, date à ajouter]

            """
            decalage = 1  # sert à compenser l'aberration des temps qui veut qu'on marque sur la fin d'une période (ex: à 24h, la pollution de 23 à minuit)
            if freq == 'T' or freq == '15T':
                f = pd.tseries.offsets.Minute
                decalage = 15
            if freq == 'H':
                f = pd.tseries.offsets.Hour
            if freq == 'D':
                f = pd.tseries.offsets.Day
            if freq == 'M':
                f = pd.tseries.offsets.MonthBegin
            if freq == 'A':
                f = pd.tseries.offsets.YearBegin
            else:
                f = pd.tseries.offsets.Hour
            new_index = [date + f(int(delta) - decalage) for date, delta in index]
            return new_index

        # Reformatage du champ des noms de mesure
        mes = _format(mes)

        # Analyse des champs dates
        debut = to_date(debut, dayfirst, format)
        if not fin:
            fin = debut
        else:
            fin = to_date(fin, dayfirst, format)


        # La freq de temps Q n'existe pas, on passe d'abord par une fréquence 15 minutes
        if freq in ('Q', 'T'):
            freq = '15T'

        # Sélection des champs et de la table en fonctions de la fréquence de temps souhaitée
        if freq == '15T':
            diviseur = 96
            champ_val = ','.join(['Q_M%02i AS "%i"' % (x, x * 15) for x in range(1, diviseur + 1)])
            champ_code = 'Q_ETATV'
            table = 'JOURNALIER'
        elif freq == 'H':
            diviseur = 24
            champ_val = ','.join(['H_M%02i AS "%i"' % (x, x) for x in range(1, diviseur + 1)])
            champ_code = 'H_ETAT'
            table = 'JOURNALIER'
        elif freq == 'D':
            diviseur = 1
            champ_val = 'J_M01 AS "1"'
            champ_code = 'J_ETAT'
            table = 'JOURNALIER'
        elif freq == 'M':
            diviseur = 12
            champ_val = ','.join(['M_M%02i AS "%i"' % (x, x) for x in range(1, diviseur + 1)])
            champ_code = 'M_ETAT'
            table = 'MOIS'
        elif freq == 'A':
            diviseur = 1
            champ_val = 'A_M01 AS "1"'
            champ_code = 'A_ETAT'
            table = 'MOIS'
        else:
            raise ValueError("freq doit être T, H, D, M ou A")

        if table == 'JOURNALIER':
            champ_date = 'J_DATE'
            debut_db = debut
            fin_db = fin
        else:
            champ_date = 'M_DATE'
            # Pour les freq='M' et 'A', la table contient toutes les valeurs sur une
            # année entière. Pour ne pas perturber la récupération si on passait des
            # dates en milieu d'année, on transforme les dates pour être calées en début
            # et en fin d'année. Le recadrage se fera plus loin dans le code, lors du reindex
            debut_db = debut.replace(month=1, day=1, hour=0, minute=0)
            fin_db = fin.replace(month=12, day=31, hour=23, minute=0)

        debut_db = debut_db.strftime("%Y-%m-%d")
        fin_db = fin_db.strftime("%Y-%m-%d")

        # Récupération des valeurs et codes d'états associés
        _sql = """SELECT
        IDENTIFIANT as "id",
        {champ_date} as "date",
        {champ_code} as "etat",
        {champ_val}
        FROM {table}
        INNER JOIN MESURE USING (NOM_COURT_MES)
        WHERE IDENTIFIANT IN ('{mes}')
        AND {champ_date} BETWEEN TO_DATE('{debut}', 'YYYY-MM-DD') AND TO_DATE('{fin}', 'YYYY-MM-DD')
        ORDER BY IDENTIFIANT, {champ_date} ASC""".format(champ_date=champ_date,
                                                         table=table,
                                                         champ_code=champ_code,
                                                         mes=mes,
                                                         champ_val=champ_val,
                                                         debut=debut_db,
                                                         fin=fin_db)
        ## TODO : A essayer quand la base sera en version 11g
        # _sql = """SELECT *
        # FROM ({selection})
        # UNPIVOT (IDENTIFIANT FOR VAL IN ({champ_as}))""".format(selection=_sql,
        # champ_date=champ_date,
        # champ_as=champ_as)

        # On recupere les valeurs depuis la freq dans une dataframe
        rep = psql.read_sql(_sql, self.conn)

        # On créait un multiindex pour manipuler plus facilement le dataframe
        df = rep.set_index(['id', 'date'])

        # Stack le dataframe pour mettre les colonnes en lignes, en supprimant la colonne des états
        # puis on unstack suivant l'id pour avoir les polluants en colonnes
        etats = df['etat']
        df = df.drop('etat', axis=1)
        df_stack = df.stack(dropna=False)
        df = df_stack.unstack('id')

        # Calcul d'un nouvel index avec les bonnes dates. L'index du df est
        # formé du champ date à minuit, et des noms des champs de valeurs
        # qui sont aliassés de 1 à 24 pour les heures, ... voir champ_val.
        # On aggrève alors ces 2 valeurs pour avoir des dates alignées qu'on utilise alors comme index final
        index = create_index(df.index, freq)
        df.reset_index(inplace=True, drop=True)
        df['date'] = index
        df = df.set_index(['date'])
        # Traitement des codes d'état
        # On concatène les codes d'état pour chaque polluant
        # etats = etats.sum(level=0)
        # etats = pd.DataFrame(zip(*etats.apply(list)))
        etats = etats.unstack('id')
        etats.fillna(value=MISSING_CODE * diviseur, inplace=True)
        etats = etats.sum(axis=0)
        etats = pd.DataFrame(list(zip(*etats.apply(list))))
        etats.index = df.index
        etats.columns = df.columns

        # Remplacement des valeurs aux dates manquantes par des NaN
        dates_completes = date_range(debut, fin, freq)
        df = df.reindex(dates_completes)
        etats = etats.reindex(dates_completes)

        # Invalidation par codes d'état
        # Pour chaque code d'état, regarde si oui ou non il est invalidant en le remplacant par un booléen
        invalid = etats_to_invalid(etats)

        if not brut:
            # dans le dataframe, masque toute valeur invalide par NaN
            dfn = df.mask(invalid)  # DataFrame net
            return dfn
        else:
            return df, etats