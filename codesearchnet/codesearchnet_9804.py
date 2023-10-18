def homogenize_stops_table_with_other_db(self, source):
        """
        This function takes an external database, looks of common stops and adds the missing stops to both databases.
        In addition the stop_pair_I column is added. This id links the stops between these two sources.
        :param source: directory of external database
        :return:
        """
        cur = self.conn.cursor()
        self.attach_gtfs_database(source)

        query_inner_join = """SELECT t1.*
                              FROM stops t1
                              INNER JOIN other.stops t2
                              ON t1.stop_id=t2.stop_id
                              AND find_distance(t1.lon, t1.lat, t2.lon, t2.lat) <= 50"""
        df_inner_join = self.execute_custom_query_pandas(query_inner_join)
        print("number of common stops: ", len(df_inner_join.index))
        df_not_in_other = self.execute_custom_query_pandas("SELECT * FROM stops EXCEPT " + query_inner_join)
        print("number of stops missing in second feed: ", len(df_not_in_other.index))
        df_not_in_self = self.execute_custom_query_pandas("SELECT * FROM other.stops EXCEPT " +
                                                          query_inner_join.replace("t1.*", "t2.*"))
        print("number of stops missing in first feed: ", len(df_not_in_self.index))
        try:
            self.execute_custom_query("""ALTER TABLE stops ADD COLUMN stop_pair_I INT """)

            self.execute_custom_query("""ALTER TABLE other.stops ADD COLUMN stop_pair_I INT """)
        except sqlite3.OperationalError:
            pass
        stop_id_stub = "added_stop_"
        counter = 0
        rows_to_update_self = []
        rows_to_update_other = []
        rows_to_add_to_self = []
        rows_to_add_to_other = []

        for items in df_inner_join.itertuples(index=False):
            rows_to_update_self.append((counter, items[1]))
            rows_to_update_other.append((counter, items[1]))
            counter += 1

        for items in df_not_in_other.itertuples(index=False):
            rows_to_update_self.append((counter, items[1]))
            rows_to_add_to_other.append((stop_id_stub + str(counter),) + tuple(items[x] for x in [2, 3, 4, 5, 6, 8, 9])
                                        + (counter,))
            counter += 1

        for items in df_not_in_self.itertuples(index=False):
            rows_to_update_other.append((counter, items[1]))
            rows_to_add_to_self.append((stop_id_stub + str(counter),) + tuple(items[x] for x in [2, 3, 4, 5, 6, 8, 9])
                                       + (counter,))
            counter += 1

        query_add_row = """INSERT INTO stops(
                                    stop_id,
                                    code,
                                    name,
                                    desc,
                                    lat,
                                    lon,
                                    location_type,
                                    wheelchair_boarding,
                                    stop_pair_I) VALUES (%s) """ % (", ".join(["?" for x in range(9)]))

        query_update_row = """UPDATE stops SET stop_pair_I=? WHERE stop_id=?"""
        print("adding rows to databases")
        cur.executemany(query_add_row, rows_to_add_to_self)
        cur.executemany(query_update_row, rows_to_update_self)
        cur.executemany(query_add_row.replace("stops", "other.stops"), rows_to_add_to_other)
        cur.executemany(query_update_row.replace("stops", "other.stops"), rows_to_update_other)
        self.conn.commit()
        print("finished")