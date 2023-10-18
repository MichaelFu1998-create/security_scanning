def finalize(self, neighbor_label_bags=None, walk_durations=None, departure_arrival_stop_pairs=None):
        """
        Parameters
        ----------
        neighbor_label_bags: list
            each list element is a list of labels corresponding to a neighboring node
             (note: only labels with first connection being a departure should be included)
        walk_durations: list
        departure_arrival_stop_pairs: list of tuples
        Returns
        -------
        None
        """
        assert (not self._finalized)
        if self._final_pareto_optimal_labels is None:
            self._compute_real_connection_labels()
        if neighbor_label_bags is not None:
            assert (len(walk_durations) == len(neighbor_label_bags))
            self._compute_final_pareto_optimal_labels(neighbor_label_bags,
                                                      walk_durations,
                                                      departure_arrival_stop_pairs)
        else:
            self._final_pareto_optimal_labels = self._real_connection_labels
        self._finalized = True
        self._closed = True