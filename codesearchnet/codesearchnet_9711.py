def _scan_footpaths_to_departure_stop(self, connection_dep_stop, connection_dep_time, arrival_time_target):
        """ A helper method for scanning the footpaths. Updates self._stop_profiles accordingly"""
        for _, neighbor, data in self._walk_network.edges_iter(nbunch=[connection_dep_stop],
                                                               data=True):
            d_walk = data['d_walk']
            neighbor_dep_time = connection_dep_time - d_walk / self._walk_speed
            pt = LabelTimeSimple(departure_time=neighbor_dep_time, arrival_time_target=arrival_time_target)
            self._stop_profiles[neighbor].update_pareto_optimal_tuples(pt)