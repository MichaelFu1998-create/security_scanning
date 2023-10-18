def get_transfer_stop_pairs(self):
        """
        Get stop pairs through which transfers take place

        Returns
        -------
        transfer_stop_pairs: list
        """
        transfer_stop_pairs = []
        previous_arrival_stop = None
        current_trip_id = None
        for leg in self.legs:
            if leg.trip_id is not None and leg.trip_id != current_trip_id and previous_arrival_stop is not None:
                transfer_stop_pair = (previous_arrival_stop, leg.departure_stop)
                transfer_stop_pairs.append(transfer_stop_pair)
            previous_arrival_stop = leg.arrival_stop
            current_trip_id = leg.trip_id
        return transfer_stop_pairs