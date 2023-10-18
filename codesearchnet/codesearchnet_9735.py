def update_pareto_optimal_tuples(self, new_label):
        """
        Parameters
        ----------
        new_label: LabelTime

        Returns
        -------
        updated: bool
        """
        assert (isinstance(new_label, LabelTime))
        if self._labels:
            assert (new_label.departure_time <= self._labels[-1].departure_time)
            best_later_departing_arrival_time = self._labels[-1].arrival_time_target
        else:
            best_later_departing_arrival_time = float('inf')

        walk_to_target_arrival_time = new_label.departure_time + self._walk_to_target_duration

        best_arrival_time = min(walk_to_target_arrival_time,
                                best_later_departing_arrival_time,
                                new_label.arrival_time_target)
        # this should be changed to get constant time insertions / additions
        # (with time-indexing)
        if (new_label.arrival_time_target < walk_to_target_arrival_time and
                new_label.arrival_time_target < best_later_departing_arrival_time):
            self._labels.append(LabelTime(new_label.departure_time, best_arrival_time))
            return True
        else:
            return False