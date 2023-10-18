def _run(self):
        """
        Run the actual simulation.
        """
        if self._has_run:
            raise RuntimeError("This spreader instance has already been run: "
                               "create a new Spreader object for a new run.")
        i = 1
        while self.event_heap.size() > 0 and len(self._uninfected_stops) > 0:
            event = self.event_heap.pop_next_event()
            this_stop = self._stop_I_to_spreading_stop[event.from_stop_I]

            if event.arr_time_ut > self.start_time_ut + self.max_duration_ut:
                break

            if this_stop.can_infect(event):

                target_stop = self._stop_I_to_spreading_stop[event.to_stop_I]
                already_visited = target_stop.has_been_visited()
                target_stop.visit(event)

                if not already_visited:
                    self._uninfected_stops.remove(event.to_stop_I)
                    print(i, self.event_heap.size())
                    transfer_distances = self.gtfs.get_straight_line_transfer_distances(event.to_stop_I)
                    self.event_heap.add_walk_events_to_heap(transfer_distances, event, self.start_time_ut,
                                                            self.walk_speed, self._uninfected_stops,
                                                            self.max_duration_ut)
                    i += 1
        self._has_run = True