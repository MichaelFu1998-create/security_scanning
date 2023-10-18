def get_straight_line_transfer_distances(self, stop_I=None):
        """
        Get (straight line) distances to stations that can be transferred to.

        Parameters
        ----------
        stop_I : int, optional
            If not specified return all possible transfer distances

        Returns
        -------
        distances: pandas.DataFrame
            each row has the following items
                from_stop_I: int
                to_stop_I: int
                d: float or int #distance in meters
        """
        if stop_I is not None:
            query = u""" SELECT from_stop_I, to_stop_I, d
                        FROM stop_distances
                            WHERE
                                from_stop_I=?
                    """
            params = (u"{stop_I}".format(stop_I=stop_I),)
        else:
            query = """ SELECT from_stop_I, to_stop_I, d
                        FROM stop_distances
                    """
            params = None
        stop_data_df = pd.read_sql_query(query, self.conn, params=params)
        return stop_data_df