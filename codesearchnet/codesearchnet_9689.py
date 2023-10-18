def visit(self, event):
        """
        Visit the stop if it has not been visited already by an event with
        earlier arr_time_ut (or with other trip that does not require a transfer)

        Parameters
        ----------
        event : Event
            an instance of the Event (namedtuple)

        Returns
        -------
        visited : bool
            if visit is stored, returns True, otherwise False
        """
        to_visit = False
        if event.arr_time_ut <= self.min_transfer_time+self.get_min_visit_time():
            to_visit = True
        else:
            for ve in self.visit_events:
                if (event.trip_I == ve.trip_I) and event.arr_time_ut < ve.arr_time_ut:
                    to_visit = True

        if to_visit:
            self.visit_events.append(event)
            min_time = self.get_min_visit_time()
            # remove any visits that are 'too old'
            self.visit_events = [v for v in self.visit_events if v.arr_time_ut <= min_time+self.min_transfer_time]
        return to_visit