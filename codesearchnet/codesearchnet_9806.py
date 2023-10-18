def insert_data(self, travel_impedance_measure_name, data):
        """
        Parameters
        ----------
        travel_impedance_measure_name: str
        data: list[dict]
            Each list element must contain keys:
            "from_stop_I", "to_stop_I", "min", "max", "median" and "mean"
        """
        f = float
        data_tuple = [(int(x["from_stop_I"]), int(x["to_stop_I"]), f(x["min"]), f(x["max"]), f(x["median"]), f(x["mean"])) for
                      x in data]
        insert_stmt = '''INSERT OR REPLACE INTO ''' + travel_impedance_measure_name + ''' (
                              from_stop_I,
                              to_stop_I,
                              min,
                              max,
                              median,
                              mean) VALUES (?, ?, ?, ?, ?, ?) '''
        self.conn.executemany(insert_stmt, data_tuple)
        self.conn.commit()