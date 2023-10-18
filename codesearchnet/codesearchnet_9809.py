def _check_dep_time_is_valid(self, dep_time):
        """
        A simple checker, that connections are coming in descending order of departure time
        and that no departure time has been "skipped".

        Parameters
        ----------
        dep_time

        Returns
        -------
        None
        """
        assert dep_time <= self._min_dep_time, "Labels should be entered in decreasing order of departure time."
        dep_time_index = self.dep_times_to_index[dep_time]
        if self._min_dep_time < float('inf'):
            min_dep_index = self.dep_times_to_index[self._min_dep_time]
            assert min_dep_index == dep_time_index or (min_dep_index == dep_time_index - 1), \
                "dep times should be ordered sequentially"
        else:
            assert dep_time_index is 0, "first dep_time index should be zero (ensuring that all connections are properly handled)"
        self._min_dep_time = dep_time