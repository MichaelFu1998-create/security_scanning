def get_indices(self, res, debut, fin):
        """
        Récupération des indices ATMO pour un réseau donné.

        Paramètres:
        res : Nom du ou des réseaux à chercher (str, list, pandas.Series)
        debut: date de début, format YYYY-MM-JJ (str)
        fin: Date de fin, format YYYY-MM-JJ (str)

        """
        res = _format(res)

        _sql = """SELECT
        J_DATE AS "date",
        NOM_AGGLO AS "reseau",
        C_IND_CALCULE AS "indice"
        FROM RESULTAT_INDICE
        INNER JOIN GROUPE_ATMO USING (NOM_COURT_GRP)
        WHERE NOM_AGGLO IN ('%s')
        AND J_DATE BETWEEN TO_DATE('%s', 'YYYY-MM-DD') AND TO_DATE('%s', 'YYYY-MM-DD') """ % (res, debut, fin)
        rep = psql.read_sql(_sql, self.conn)
        df = rep.set_index(['reseau', 'date'])
        df = df['indice']
        df = df.unstack('reseau')
        dates_completes = date_range(to_date(debut), to_date(fin), freq='D')
        df = df.reindex(dates_completes)
        return df