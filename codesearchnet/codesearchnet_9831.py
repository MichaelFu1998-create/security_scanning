def _scan_footpaths(self, stop_id, walk_departure_time):
        """
        Scan the footpaths originating from stop_id

        Parameters
        ----------
        stop_id: int
        """
        for _, neighbor, data in self._walk_network.edges_iter(nbunch=[stop_id], data=True):
            d_walk = data["d_walk"]
            arrival_time = walk_departure_time + d_walk / self._walk_speed
            self._update_stop_label(neighbor, arrival_time)