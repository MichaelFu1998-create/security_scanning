def liste_parametres(self, parametre=None):
        """
        Liste des param�tres

        Param�tres:
        parametre: si fourni, retourne l'entr�e pour ce parametre uniquement

        """
        condition = ""
        if parametre:
            condition = "WHERE CCHIM='%s'" % parametre
        _sql = """SELECT CCHIM AS PARAMETRE,
        NCON AS LIBELLE,
        NOPOL AS CODE
        FROM NOM_MESURE %s ORDER BY CCHIM""" % condition
        return psql.read_sql(_sql, self.conn)