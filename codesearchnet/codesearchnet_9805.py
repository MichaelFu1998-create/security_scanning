def read_data_as_dataframe(self,
                               travel_impedance_measure,
                               from_stop_I=None,
                               to_stop_I=None,
                               statistic=None):
        """
        Recover pre-computed travel_impedance between od-pairs from the database.

        Returns
        -------
        values: number | Pandas DataFrame
        """
        to_select = []
        where_clauses = []
        to_select.append("from_stop_I")
        to_select.append("to_stop_I")
        if from_stop_I is not None:
            where_clauses.append("from_stop_I=" + str(int(from_stop_I)))
        if to_stop_I is not None:
            where_clauses.append("to_stop_I=" + str(int(to_stop_I)))
        where_clause = ""
        if len(where_clauses) > 0:
            where_clause = " WHERE " + " AND ".join(where_clauses)
        if not statistic:
            to_select.extend(["min", "mean", "median", "max"])
        else:
            to_select.append(statistic)
        to_select_clause = ",".join(to_select)
        if not to_select_clause:
            to_select_clause = "*"
        sql = "SELECT " + to_select_clause + " FROM " + travel_impedance_measure + where_clause + ";"
        df = pd.read_sql(sql, self.conn)
        return df