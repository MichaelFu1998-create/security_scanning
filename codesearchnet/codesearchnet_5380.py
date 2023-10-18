def get_outgoing_sequence_names(self):
        """
        Returns a list of the names of outgoing sequences. Some may be None.
        """
        return sorted([s.name for s in
                       list(self.outgoing_sequence_flows_by_id.values())])