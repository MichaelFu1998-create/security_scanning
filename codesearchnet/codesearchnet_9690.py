def can_infect(self, event):
        """
        Whether the spreading stop can infect using this event.
        """
        if event.from_stop_I != self.stop_I:
            return False

        if not self.has_been_visited():
            return False
        else:
            time_sep = event.dep_time_ut-self.get_min_visit_time()
            # if the gap between the earliest visit_time and current time is
            # smaller than the min. transfer time, the stop can pass the spreading
            # forward
            if (time_sep >= self.min_transfer_time) or (event.trip_I == -1 and time_sep >= 0):
                return True
            else:
                for visit in self.visit_events:
                    # if no transfer, please hop-on
                    if (event.trip_I == visit.trip_I) and (time_sep >= 0):
                        return True
            return False