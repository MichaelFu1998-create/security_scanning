def add_event(self, event):
        """
        Add an event to the heap/priority queue

        Parameters
        ----------
        event : Event
        """
        assert event.dep_time_ut <= event.arr_time_ut
        heappush(self.heap, event)