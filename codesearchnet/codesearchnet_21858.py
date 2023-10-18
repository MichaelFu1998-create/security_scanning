def liste_campagnes(self, campagne=None):
        """
        Liste des campagnes de mesure et des stations associées

        Paramètres:
        campagne: Si définie, liste des stations que pour cette campagne

        """

        condition = ""
        if campagne:
            condition = "WHERE NOM_COURT_CM='%s' """ % campagne
        _sql = """SELECT
        NOM_COURT_CM AS CAMPAGNE,
        IDENTIFIANT AS STATION,
        LIBELLE AS LIBELLE_CM,
        DATEDEB AS DEBUT,
        DATEFIN AS FIN
        FROM CAMPMES
        INNER JOIN CAMPMES_STATION USING (NOM_COURT_CM)
        INNER JOIN STATION USING (NOM_COURT_SIT)
        %s ORDER BY DATEDEB DESC""" % condition
        return psql.read_sql(_sql, self.conn)