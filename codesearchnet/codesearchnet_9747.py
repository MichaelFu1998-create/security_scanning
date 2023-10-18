def update_pareto_optimal_tuples(self, new_pareto_tuple):
        """
        # this function should be optimized

        Parameters
        ----------
        new_pareto_tuple: LabelTimeSimple

        Returns
        -------
        added: bool
            whether new_pareto_tuple was added to the set of pareto-optimal tuples
        """
        if new_pareto_tuple.duration() > self._walk_to_target_duration:
            direct_walk_label = self._label_class.direct_walk_label(new_pareto_tuple.departure_time,
                                                                    self._walk_to_target_duration)
            if not direct_walk_label.dominates(new_pareto_tuple):
                raise
        direct_walk_label = self._label_class.direct_walk_label(new_pareto_tuple.departure_time, self._walk_to_target_duration)
        if direct_walk_label.dominates(new_pareto_tuple):
            return False

        if self._new_paretotuple_is_dominated_by_old_tuples(new_pareto_tuple):
            return False
        else:
            self._remove_old_tuples_dominated_by_new_and_insert_new_paretotuple(new_pareto_tuple)
            return True