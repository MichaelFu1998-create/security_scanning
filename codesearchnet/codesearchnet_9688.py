def get_min_visit_time(self):
        """
        Get the earliest visit time of the stop.
        """
        if not self.visit_events:
            return float('inf')
        else:
            return min(self.visit_events, key=lambda event: event.arr_time_ut).arr_time_ut