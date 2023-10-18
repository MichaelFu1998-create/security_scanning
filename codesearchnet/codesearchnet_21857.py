def liste_stations(self, station=None, detail=False):
        """
        Liste des stations

        Paramètres:
        station : un nom de station valide (si vide, liste toutes les stations)
        detail : si True, affiche plus de détail sur la (les) station(s).

        """
        condition = ""
        if station:
            station = _format(station)
            condition = "WHERE IDENTIFIANT IN ('%s')" % station

        select = ""
        if detail:
            select = """,
            ISIT AS DESCRIPTION,
            NO_TELEPHONE AS TELEPHONE,
            ADRESSE_IP,
            LONGI AS LONGITUDE,
            LATI AS LATITUDE,
            ALTI AS ALTITUDE,
            AXE AS ADR,
            CODE_POSTAL AS CP,
            FLAG_VALID AS VALID"""

        _sql = """SELECT
        NSIT AS NUMERO,
        IDENTIFIANT AS STATION %s
        FROM STATION
        %s
        ORDER BY NSIT""" % (select, condition)
        return psql.read_sql(_sql, self.conn)