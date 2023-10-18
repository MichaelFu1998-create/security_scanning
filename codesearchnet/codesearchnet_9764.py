def add_leg(self, leg):
        """
        Parameters
        ----------
        leg: Connection
        """
        assert(isinstance(leg, Connection))
        if not self.legs:
            self.departure_time = leg.departure_time
        self.arrival_time = leg.arrival_time
        if leg.trip_id and (not self.legs or (leg.trip_id != self.legs[-1].trip_id)):
            self.n_boardings += 1
        self.arrival_time = leg.arrival_time
        self.legs.append(leg)