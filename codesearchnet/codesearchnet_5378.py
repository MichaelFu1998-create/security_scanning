def connect_outgoing(self, taskspec, sequence_flow_id, sequence_flow_name,
                         documentation):
        """
        Connect this task spec to the indicated child.

        :param sequence_flow_id: The ID of the connecting sequenceFlow node.

        :param sequence_flow_name: The name of the connecting sequenceFlow
        node.
        """
        self.connect(taskspec)
        s = SequenceFlow(
            sequence_flow_id, sequence_flow_name, documentation, taskspec)
        self.outgoing_sequence_flows[taskspec.name] = s
        self.outgoing_sequence_flows_by_id[sequence_flow_id] = s