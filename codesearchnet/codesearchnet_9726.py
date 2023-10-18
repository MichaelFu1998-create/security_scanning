def _finalize_profiles(self):
        """
        Deal with the first walks by joining profiles to other stops within walking distance.
        """
        for stop, stop_profile in self._stop_profiles.items():
            assert (isinstance(stop_profile, NodeProfileMultiObjective))
            neighbor_label_bags = []
            walk_durations_to_neighbors = []
            departure_arrival_stop_pairs = []
            if stop_profile.get_walk_to_target_duration() != 0 and stop in self._walk_network.node:
                neighbors = networkx.all_neighbors(self._walk_network, stop)
                for neighbor in neighbors:
                    neighbor_profile = self._stop_profiles[neighbor]
                    assert (isinstance(neighbor_profile, NodeProfileMultiObjective))
                    neighbor_real_connection_labels = neighbor_profile.get_labels_for_real_connections()
                    neighbor_label_bags.append(neighbor_real_connection_labels)
                    walk_durations_to_neighbors.append(int(self._walk_network.get_edge_data(stop, neighbor)["d_walk"] /
                                                       self._walk_speed))
                    departure_arrival_stop_pairs.append((stop, neighbor))
            stop_profile.finalize(neighbor_label_bags, walk_durations_to_neighbors, departure_arrival_stop_pairs)