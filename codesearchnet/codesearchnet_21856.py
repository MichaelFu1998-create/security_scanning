def liste_mesures(self, reseau=None, station=None, parametre=None, mesure=None):
        """
        Décrit les mesures:
        - d'un ou des reseaux,
        - d'une ou des stations,
        - d'un ou des parametres
        ou décrit une (des) mesures suivant son (leur) identifiant(s)
        Chaque attribut peut être étendu en rajoutant des noms séparés par des
        virgules ou en les mettant dans une liste/tuple/pandas.Series.
        Ainsi pour avoir la liste des mesures en vitesse et direction de vent:
        parametre="VV,DV" ou = ["VV", "DV"]
        Les arguments sont combinés ensemble pour la sélection des mesures.

        Paramètres:
        reseau : nom du reseau dans lequel lister les mesures
        station: nom de la station où lister les mesures
        parametre: Code chimique du parametre à lister
        mesure: nom de la mesure à décrire

        """

        tbreseau = ""
        conditions = []

        if reseau:
            reseau = _format(reseau)
            
            tbreseau = """INNER JOIN RESEAUMES R USING (NOM_COURT_MES) """
            conditions.append("""R.NOM_COURT_RES IN ('%s') """ % reseau)

        if parametre:
            parametre = _format(parametre)
            conditions.append("""N.CCHIM IN ('%s')""" % parametre)

        if station:
            station = _format(station)
            conditions.append("""S.IDENTIFIANT IN ('%s')""" % station)

        if mesure:
            mesure = _format(mesure)
            conditions.append("""M.IDENTIFIANT IN ('%s')""" % mesure)

        condition = "WHERE %s" % " and ".join(conditions) if conditions else ""

        _sql = """SELECT
        M.IDENTIFIANT AS MESURE,
        M.NOM_MES AS LIBELLE,
        M.UNITE AS UNITE,
        S.IDENTIFIANT AS STATION,
        N.CCHIM AS CODE_PARAM,
        N.NCON AS PARAMETRE
        FROM MESURE M
        INNER JOIN NOM_MESURE N USING (NOPOL)
        INNER JOIN STATION S USING (NOM_COURT_SIT)
        %s
        %s
        ORDER BY M.IDENTIFIANT""" % (tbreseau, condition)

        return psql.read_sql(_sql, self.conn)