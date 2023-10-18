def get_manuelles(self, site, code_parametre, debut, fin, court=False):
        """
        Recupération des mesures manuelles (labo) pour un site

        site: numéro du site (voir fonction liste_sites_prelevement)
        code_parametre: code ISO du paramètre à rechercher (C6H6=V4)
        debut: date de début du premier prélèvement
        fin: date de fin du dernier prélèvement
        court: Renvoie un tableau au format court ou long (colonnes)

        """

        condition = "WHERE MESLA.NOPOL='%s' " % code_parametre
        condition += "AND SITMETH.NSIT=%s " % site
        condition += "AND PRELEV.DATE_DEB>=TO_DATE('%s', 'YYYY-MM-DD') " % debut
        condition += "AND PRELEV.DATE_FIN<=TO_DATE('%s', 'YYYY-MM-DD') " % fin
        if court == False:
            select = """SELECT
                        MESLA.LIBELLE AS MESURE,
                        METH.LIBELLE AS METHODE,
                        ANA.VALEUR AS VALEUR,
                        MESLA.UNITE AS UNITE,
                        ANA.CODE_QUALITE AS CODE_QUALITE,
                        ANA.DATE_ANA AS DATE_ANALYSE,
                        ANA.ID_LABO AS LABO,
                        PRELEV.DATE_DEB AS DEBUT,
                        PRELEV.DATE_FIN AS FIN,
                        ANA.COMMENTAIRE AS COMMENTAIRE,
                        SITE.LIBELLE AS SITE,
                        SITE.AXE AS ADRESSE,
                        COM.NOM_COMMUNE AS COMMUNE"""
        else:
            select = """SELECT
                        MESLA.LIBELLE AS MESURE,
                        ANA.VALEUR AS VALEUR,
                        MESLA.UNITE AS UNITE,
                        ANA.CODE_QUALITE AS CODE_QUALITE,
                        PRELEV.DATE_DEB AS DEBUT,
                        PRELEV.DATE_FIN AS FIN,
                        SITE.AXE AS ADRESSE,
                        COM.NOM_COMMUNE AS COMMUNE"""
        _sql = """%s
        FROM ANALYSE ANA
        INNER JOIN PRELEVEMENT PRELEV ON (ANA.CODE_PRELEV=PRELEV.CODE_PRELEV AND ANA.CODE_SMP=PRELEV.CODE_SMP)
        INNER JOIN MESURE_LABO MESLA ON (ANA.CODE_MES_LABO=MESLA.CODE_MES_LABO AND ANA.CODE_SMP=MESLA.CODE_SMP)
        INNER JOIN SITE_METH_PRELEV SITMETH ON (ANA.CODE_SMP=SITMETH.CODE_SMP)
        INNER JOIN METH_PRELEVEMENT METH ON (SITMETH.CODE_METH_P=METH.CODE_METH_P)
        INNER JOIN SITE_PRELEVEMENT SITE ON (SITE.NSIT=SITMETH.NSIT)
        INNER JOIN COMMUNE COM ON (COM.NINSEE=SITE.NINSEE)
        %s
        ORDER BY MESLA.NOPOL,MESLA.LIBELLE,PRELEV.DATE_DEB""" % (select, condition)
        return psql.read_sql(_sql, self.conn)