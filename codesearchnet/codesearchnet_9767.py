def get_time_profile_analyzer(self, max_n_boardings=None):
        """
        Parameters
        ----------
        max_n_boardings: int
            The maximum number of boardings allowed for the labels used to construct the "temporal distance profile"

        Returns
        -------
        analyzer: NodeProfileAnalyzerTime
        """
        if max_n_boardings is None:
            max_n_boardings = self.max_trip_n_boardings()
        # compute only if not yet computed
        if not max_n_boardings in self._n_boardings_to_simple_time_analyzers:
            if max_n_boardings == 0:
                valids = []
            else:
                candidate_labels = [LabelTimeSimple(label.departure_time, label.arrival_time_target)
                                    for label in self._node_profile_final_labels if
                                    ((self.start_time_dep <= label.departure_time)
                                     and label.n_boardings <= max_n_boardings)]
                valids = compute_pareto_front(candidate_labels)
            valids.sort(key=lambda label: -label.departure_time)
            profile = NodeProfileSimple(self._walk_to_target_duration)
            for valid in valids:
                profile.update_pareto_optimal_tuples(valid)
            npat = NodeProfileAnalyzerTime.from_profile(profile, self.start_time_dep, self.end_time_dep)
            self._n_boardings_to_simple_time_analyzers[max_n_boardings] = npat
        return self._n_boardings_to_simple_time_analyzers[max_n_boardings]