def get_upstream_stops_ratio(self, target, trough_stops, ratio):
        """
        Selects the stops for which the ratio or higher proportion of trips to the target passes trough a set of trough stops
        :param target: target of trips
        :param trough_stops: stops where the selected trips are passing trough
        :param ratio: threshold for inclusion
        :return:
        """
        if isinstance(trough_stops, list):
            trough_stops = ",".join(trough_stops)
        query = """SELECT stops.* FROM other.stops, 
                    (SELECT q2.from_stop_I AS stop_I FROM 
                    (SELECT journeys.from_stop_I, count(*) AS n_total FROM journeys
                    WHERE journeys.to_stop_I = {target} 
                    GROUP BY from_stop_I) q1,
                    (SELECT journeys.from_stop_I, count(*) AS n_trough FROM journeys, legs 
                    WHERE journeys.journey_id=legs.journey_id AND legs.from_stop_I IN ({trough_stops}) AND journeys.to_stop_I = {target}
                    GROUP BY journeys.from_stop_I) q2
                    WHERE q1.from_stop_I = q2.from_stop_I AND n_trough/(n_total*1.0) >= {ratio}) q1
                    WHERE stops.stop_I = q1.stop_I""".format(target=target, trough_stops=trough_stops, ratio=ratio)
        df = read_sql_query(query, self.conn)
        return df