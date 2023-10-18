def get_segment_count_data(self, start, end, use_shapes=True):
        """
        Get segment data including PTN vehicle counts per segment that are
        fully _contained_ within the interval (start, end)

        Parameters
        ----------
        start : int
            start time of the simulation in unix time
        end : int
            end time of the simulation in unix time
        use_shapes : bool, optional
            whether to include shapes (if available)

        Returns
        -------
        seg_data : list
            each element in the list is a dict containing keys:
                "trip_I", "lats", "lons", "shape_id", "stop_seqs", "shape_breaks"
        """
        cur = self.conn.cursor()
        # get all possible trip_ids that take place between start and end
        trips_df = self.get_tripIs_active_in_range(start, end)
        # stop_I -> count, lat, lon, name
        segment_counts = Counter()
        seg_to_info = {}
        # tripI_to_seq = "inverted segToShapeData"
        tripI_to_seq = defaultdict(list)

        # loop over all trips:
        for row in trips_df.itertuples():
            # get stop_data and store it:
            stops_df = self.get_trip_stop_time_data(row.trip_I, row.day_start_ut)
            for i in range(len(stops_df) - 1):
                (stop_I, dep_time_ut, s_lat, s_lon, s_seq, shape_break) = stops_df.iloc[i]
                (stop_I_n, dep_time_ut_n, s_lat_n, s_lon_n, s_seq_n, shape_break_n) = stops_df.iloc[i + 1]
                # test if _contained_ in the interval
                # overlap would read:
                #   (dep_time_ut <= end) and (start <= dep_time_ut_n)
                if (dep_time_ut >= start) and (dep_time_ut_n <= end):
                    seg = (stop_I, stop_I_n)
                    segment_counts[seg] += 1
                    if seg not in seg_to_info:
                        seg_to_info[seg] = {
                            u"trip_I": row.trip_I,
                            u"lats": [s_lat, s_lat_n],
                            u"lons": [s_lon, s_lon_n],
                            u"shape_id": row.shape_id,
                            u"stop_seqs": [s_seq, s_seq_n],
                            u"shape_breaks": [shape_break, shape_break_n]
                        }
                        tripI_to_seq[row.trip_I].append(seg)

        stop_names = {}
        for (stop_I, stop_J) in segment_counts.keys():
            for s in [stop_I, stop_J]:
                if s not in stop_names:
                    stop_names[s] = self.stop(s)[u'name'].values[0]

        seg_data = []
        for seg, count in segment_counts.items():
            segInfo = seg_to_info[seg]
            shape_breaks = segInfo[u"shape_breaks"]
            seg_el = {}
            if use_shapes and shape_breaks and shape_breaks[0] and shape_breaks[1]:
                shape = shapes.get_shape_between_stops(
                    cur,
                    segInfo[u'trip_I'],
                    shape_breaks=shape_breaks
                )
                seg_el[u'lats'] = segInfo[u'lats'][:1] + shape[u'lat'] + segInfo[u'lats'][1:]
                seg_el[u'lons'] = segInfo[u'lons'][:1] + shape[u'lon'] + segInfo[u'lons'][1:]
            else:
                seg_el[u'lats'] = segInfo[u'lats']
                seg_el[u'lons'] = segInfo[u'lons']
            seg_el[u'name'] = stop_names[seg[0]] + u"-" + stop_names[seg[1]]
            seg_el[u'count'] = count
            seg_data.append(seg_el)
        return seg_data