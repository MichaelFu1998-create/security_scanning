def evaluate(self, dep_time, first_leg_can_be_walk=True, connection_arrival_time=None):

        """
        Get the pareto_optimal set of Labels, given a departure time.

        Parameters
        ----------
        dep_time : float, int
            time in unix seconds
        first_leg_can_be_walk : bool, optional
            whether to allow walking to target to be included into the profile
            (I.e. whether this function is called when scanning a pseudo-connection:
            "double" walks are not allowed.)
        connection_arrival_time: float, int, optional
            used for computing the walking label if dep_time, i.e., connection.arrival_stop_next_departure_time, is infinity)
        connection: connection object

        Returns
        -------
        pareto_optimal_labels : set
            Set of Labels
        """
        walk_labels = list()
        # walk label towards target
        if first_leg_can_be_walk and self._walk_to_target_duration != float('inf'):
            # add walk_label
            if connection_arrival_time is not None:
                walk_labels.append(self._get_label_to_target(connection_arrival_time))
            else:
                walk_labels.append(self._get_label_to_target(dep_time))

        # if dep time is larger than the largest dep time -> only walk labels are possible
        if dep_time in self.dep_times_to_index:
            assert (dep_time != float('inf'))
            index = self.dep_times_to_index[dep_time]
            labels = self._label_bags[index]
            pareto_optimal_labels = merge_pareto_frontiers(labels, walk_labels)
        else:
            pareto_optimal_labels = walk_labels

        if not first_leg_can_be_walk:
            pareto_optimal_labels = [label for label in pareto_optimal_labels if not label.first_leg_is_walk]
        return pareto_optimal_labels