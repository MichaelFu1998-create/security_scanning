def connect_outgoing(self, outgoing_task, outgoing_task_node,
                         sequence_flow_node, is_default):
        """
        Connects this task to the indicating outgoing task, with the details in
        the sequence flow. A subclass can override this method to get extra
        information from the node.
        """
        self.task.connect_outgoing(
            outgoing_task, sequence_flow_node.get('id'),
            sequence_flow_node.get(
                'name', None),
            self.parser._parse_documentation(sequence_flow_node,
                                             task_parser=self))