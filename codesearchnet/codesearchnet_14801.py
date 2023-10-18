def get_lswitch_ids_for_network(self, context, network_id):
        """Public interface for fetching lswitch ids for a given network.

        NOTE(morgabra) This is here because calling private methods
        from outside the class feels wrong, and we need to be able to
        fetch lswitch ids for use in other drivers.
        """
        lswitches = self._lswitches_for_network(context, network_id).results()
        return [s['uuid'] for s in lswitches["results"]]