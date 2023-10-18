def add_walk_events_to_heap(self, transfer_distances, e, start_time_ut, walk_speed, uninfected_stops, max_duration_ut):
        """
        Parameters
        ----------
        transfer_distances:
        e : Event
        start_time_ut : int
        walk_speed : float
        uninfected_stops : list
        max_duration_ut : int
        """
        n = len(transfer_distances)
        dists_values = transfer_distances.values
        to_stop_I_index = np.nonzero(transfer_distances.columns == 'to_stop_I')[0][0]
        d_index = np.nonzero(transfer_distances.columns == 'd')[0][0]
        for i in range(n):
            transfer_to_stop_I = dists_values[i, to_stop_I_index]
            if transfer_to_stop_I in uninfected_stops:
                d = dists_values[i, d_index]
                transfer_arr_time = e.arr_time_ut + int(d/float(walk_speed))
                if transfer_arr_time > start_time_ut+max_duration_ut:
                    continue
                te = Event(transfer_arr_time, e.arr_time_ut, e.to_stop_I, transfer_to_stop_I, WALK)
                self.add_event(te)