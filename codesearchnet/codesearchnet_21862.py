def get_indices_et_ssi(self, reseau, debut, fin, complet=True):
        """Renvoie l'indice et les sous_indices
        complet: renvoyer les complets ou les prévus
        reseau: nom du réseau à renvoyer
        debut: date de début à renvoyer
        fin: date de fin à renvoyer

        Renvoi : reseau, date, Indice, sous_ind NO2,PM10,O3,SO2
        """
        if complet:
            i_str = "c_ind_diffuse"
            ssi_str = "c_ss_indice"
        else:
            i_str = "p_ind_diffuse"
            ssi_str = "p_ss_indice"

        _sql = """SELECT
                g.nom_agglo as "reseau",
                i.j_date as "date",
                max(case when i.{0}>0 then i.{0} else 0 end) indice,
                max(case when n.cchim='NO2' then ssi.{1} else 0 end) no2,
                max(case when n.cchim='PM10' then ssi.{1} else 0 end) pm10,
                max(case when n.cchim='O3' then ssi.{1} else 0 end) o3,
                max(case when n.cchim='SO2' then ssi.{1} else 0 end) so2
        FROM resultat_indice i
        INNER JOIN resultat_ss_indice ssi ON (i.nom_court_grp=ssi.nom_court_grp AND i.j_date=ssi.j_date)
        INNER JOIN groupe_atmo g ON (i.nom_court_grp=g.nom_court_grp)
        INNER JOIN nom_mesure n ON (ssi.nopol=n.nopol)
        WHERE g.nom_agglo='{2}'
        AND i.j_date BETWEEN
        TO_DATE('{3}', 'YYYY-MM-DD') AND
        TO_DATE('{4}', 'YYYY-MM-DD')
        GROUP BY
        g.nom_agglo,
        i.j_date
        ORDER BY i.j_date""".format(i_str, ssi_str, reseau, debut, fin)
        df = psql.read_sql(_sql, self.conn)
        df = df.set_index(['reseau', 'date'])
        return df