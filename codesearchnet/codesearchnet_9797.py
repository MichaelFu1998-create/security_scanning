def stop(self, stop_I):
        """
        Get all stop data as a pandas DataFrame for all stops, or an individual stop'

        Parameters
        ----------
        stop_I : int
            stop index

        Returns
        -------
        stop: pandas.DataFrame
        """
        return pd.read_sql_query("SELECT * FROM stops WHERE stop_I={stop_I}".format(stop_I=stop_I), self.conn)