def connect_child(self, child_node):
        """Adds a connection to an existing rule in the :class`Flow` graph.
        The given :class`Rule` subclass must be allowed to be connected at
        this stage of the flow according to the hierarchy of rules.

        :param child_node: 
            ``FlowNodeData`` to attach as a child
        """
        self._child_allowed(child_node.rule)
        self.node.connect_child(child_node.node)