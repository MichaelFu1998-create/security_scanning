def evaluate_earliest_arrival_time_at_target(self, dep_time, transfer_margin):
        """
        Get the earliest arrival time at the target, given a departure time.

        Parameters
        ----------
        dep_time : float, int
            time in unix seconds
        transfer_margin: float, int
            transfer margin in seconds

        Returns
        -------
        arrival_time : float
            Arrival time in the given time unit (seconds after unix epoch).
        """
        minimum = dep_time + self._walk_to_target_duration
        dep_time_plus_transfer_margin = dep_time + transfer_margin
        for label in self._labels:
            if label.departure_time >= dep_time_plus_transfer_margin and label.arrival_time_target < minimum:
                minimum = label.arrival_time_target
        return float(minimum)