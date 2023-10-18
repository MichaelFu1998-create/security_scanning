def liste_mesures(self, reseau=None, station=None, parametre=None, mesure=None):
        """
        D�crit les mesures:
        - d'un ou des reseaux,
        - d'une ou des stations,
        - d'un ou des parametres
        ou d�crit une (des) mesures suivant son (leur) identifiant(s)
        Chaque attribut peut �tre �tendu en rajoutant des noms s�par�s par des
        virgules ou en les mettant dans une liste/tuple/pandas.Series.
        Ainsi pour avoir la liste des mesures en vitesse et direction de vent:
        parametre="VV,DV" ou = ["VV", "DV"]
        Les arguments sont combin�s ensemble pour la s�lection des mesures.

        Param�tres:
        reseau : nom du reseau dans lequel lister les mesures
        station: nom de la station o� lister les mesures
        parametre: Code chimique du parametre � lister
        mesure: nom de la mesure � d�crire

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