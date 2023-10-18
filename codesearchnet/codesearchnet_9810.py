def update(self, new_labels, departure_time_backup=None):
        """
        Update the profile with the new labels.
        Each new label should have the same departure_time.

        Parameters
        ----------
        new_labels: list[LabelTime]

        Returns
        -------
        added: bool
            whether new_pareto_tuple was added to the set of pareto-optimal tuples
        """
        if self._closed:
            raise RuntimeError("Profile is closed, no updates can be made")
        try:
            departure_time = next(iter(new_labels)).departure_time
        except StopIteration:
            departure_time = departure_time_backup
        self._check_dep_time_is_valid(departure_time)

        for new_label in new_labels:
            assert (new_label.departure_time == departure_time)
        dep_time_index = self.dep_times_to_index[departure_time]

        if dep_time_index > 0:
            # Departure time is modified in order to not pass on labels which are not Pareto-optimal when departure time is ignored.
            mod_prev_labels = [label.get_copy_with_specified_departure_time(departure_time) for label
                               in self._label_bags[dep_time_index - 1]]
        else:
            mod_prev_labels = list()
        mod_prev_labels += self._label_bags[dep_time_index]

        walk_label = self._get_label_to_target(departure_time)
        if walk_label:
            new_labels = new_labels + [walk_label]
        new_frontier = merge_pareto_frontiers(new_labels, mod_prev_labels)

        self._label_bags[dep_time_index] = new_frontier
        return True