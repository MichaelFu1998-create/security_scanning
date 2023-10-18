def _lswitch_select_open(self, context, switches=None, **kwargs):
        """Selects an open lswitch for a network.

        Note that it does not select the most full switch, but merely one with
        ports available.
        """

        if switches is not None:
            for res in switches["results"]:
                count = res["_relations"]["LogicalSwitchStatus"]["lport_count"]
                if (self.limits['max_ports_per_switch'] == 0 or
                        count < self.limits['max_ports_per_switch']):
                    return res["uuid"]
        return None