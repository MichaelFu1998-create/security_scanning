def add_child_rule(self, child_rule):
        """Add a child path in the :class:`Flow` graph using the given 
        :class:`Rule` subclass.  This will create a new child :class:`Node` in
        the associated :class:`Flow` object's state graph with a new
        :class:`FlowNodeData` instance attached.
        
        The :class:`Rule` must be allowed at this stage of the flow according
        to the hierarchy of rules.

        :param child_rule: 
            :class:`Rule` class to add to the flow as a child of :class:`Node`
            that this object owns
        :returns: 
            ``FlowNodeData`` that was added
        """
        self._child_allowed(child_rule)
        child_node = self.node.add_child(rule_label=child_rule.class_label)
        return child_node.data