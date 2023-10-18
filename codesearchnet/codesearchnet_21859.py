def get_mesures(self, mes, debut=None, fin=None, freq='H', format=None,
                    dayfirst=False, brut=False):
        """
        R�cup�ration des donn�es de mesure.

        Param�tres:
        mes: Un nom de mesure ou plusieurs s�par�es par des virgules, une liste
            (list, tuple, pandas.Series) de noms
        debut: Chaine de caract�re ou objet datetime d�crivant la date de d�but.
            D�faut=date du jour
        fin: Chaine de caract�re ou objet datetime d�crivant la date de fin.
            D�faut=date de d�but
        freq: fr�quence de temps. '15T' | 'H' | 'D' | 'M' | 'A' (15T pour quart-horaire)
        format: chaine de caract�re d�crivant le format des dates (ex:"%Y-%m-%d"
            pour debut/fin="2013-01-28"). Appeler pyair.date.strtime_help() pour
            obtenir la liste des codes possibles.
            Defaut="%Y-%m-%d"
        dayfirst: Si aucun format n'est fourni et que les dates sont des chaines
            de caract�res, aide le d�crypteur � transformer la date en objet datetime
            en sp�cifiant que les dates commencent par le jour (ex:11/09/2012
            pourrait �tre interpret� comme le 09 novembre si dayfirst=False)
        brut: si oui ou non renvoyer le dataframe brut, non invalid�, et les
            codes d'�tat des mesures
            Defaut=False

        Retourne:
        Un dataframe contenant toutes les mesures demand�es.
        Si brut=True, renvoie le  dataframe des mesures brutes non invalid�es et
        le dataframe des codes d'�tats.
        Le dataframe valide (net) peut �tre alors recalcul� en faisant:
        brut, etats = xr.get_mesure(..., brut=True)
        invalides = etats_to_invalid(etats)
        net = brut.mask(invalides)

        """

        def create_index(index, freq):
            """
            Nouvel index [id, date] avec date format� suivant le pas de temps voulu
            index: index de l'ancien dataframe, tel que [date � minuit, date � ajouter]

            """
            decalage = 1  # sert � compenser l'aberration des temps qui veut qu'on marque sur la fin d'une p�riode (ex: � 24h, la pollution de 23 � minuit)
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


        # La freq de temps Q n'existe pas, on passe d'abord par une fr�quence 15 minutes
        if freq in ('Q', 'T'):
            freq = '15T'

        # S�lection des champs et de la table en fonctions de la fr�quence de temps souhait�e
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
            raise ValueError("freq doit �tre T, H, D, M ou A")

        if table == 'JOURNALIER':
            champ_date = 'J_DATE'
            debut_db = debut
            fin_db = fin
        else:
            champ_date = 'M_DATE'
            # Pour les freq='M' et 'A', la table contient toutes les valeurs sur une
            # ann�e enti�re. Pour ne pas perturber la r�cup�ration si on passait des
            # dates en milieu d'ann�e, on transforme les dates pour �tre cal�es en d�but
            # et en fin d'ann�e. Le recadrage se fera plus loin dans le code, lors du reindex
            debut_db = debut.replace(month=1, day=1, hour=0, minute=0)
            fin_db = fin.replace(month=12, day=31, hour=23, minute=0)

        debut_db = debut_db.strftime("%Y-%m-%d")
        fin_db = fin_db.strftime("%Y-%m-%d")

        # R�cup�ration des valeurs et codes d'�tats associ�s
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

        # On cr�ait un multiindex pour manipuler plus facilement le dataframe
        df = rep.set_index(['id', 'date'])

        # Stack le dataframe pour mettre les colonnes en lignes, en supprimant la colonne des �tats
        # puis on unstack suivant l'id pour avoir les polluants en colonnes
        etats = df['etat']
        df = df.drop('etat', axis=1)
        df_stack = df.stack(dropna=False)
        df = df_stack.unstack('id')

        # Calcul d'un nouvel index avec les bonnes dates. L'index du df est
        # form� du champ date � minuit, et des noms des champs de valeurs
        # qui sont aliass�s de 1 � 24 pour les heures, ... voir champ_val.
        # On aggr�ve alors ces 2 valeurs pour avoir des dates align�es qu'on utilise alors comme index final
        index = create_index(df.index, freq)
        df.reset_index(inplace=True, drop=True)
        df['date'] = index
        df = df.set_index(['date'])
        # Traitement des codes d'�tat
        # On concat�ne les codes d'�tat pour chaque polluant
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

        # Invalidation par codes d'�tat
        # Pour chaque code d'�tat, regarde si oui ou non il est invalidant en le remplacant par un bool�en
        invalid = etats_to_invalid(etats)

        if not brut:
            # dans le dataframe, masque toute valeur invalide par NaN
            dfn = df.mask(invalid)  # DataFrame net
            return dfn
        else:
            return df, etats