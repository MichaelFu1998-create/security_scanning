def connect_outgoing_if(self, condition, taskspec, sequence_flow_id,
                            sequence_flow_name, documentation):
        """
        Connect this task spec to the indicated child, if the condition
        evaluates to true. This should only be called if the task has a
        connect_if method (e.g. ExclusiveGateway).

        :param sequence_flow_id: The ID of the connecting sequenceFlow node.

        :param sequence_flow_name: The name of the connecting sequenceFlow
        node.
        """
        self.connect_if(_BpmnCondition(condition), taskspec)
        s = SequenceFlow(
            sequence_flow_id, sequence_flow_name, documentation, taskspec)
        self.outgoing_sequence_flows[taskspec.name] = s
        self.outgoing_sequence_flows_by_id[sequence_flow_id] = s