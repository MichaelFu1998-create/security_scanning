def start(self, flow):
        """Factory method for a running state based on a flow.  Creates and
        returns a ``State`` object and calls the associated
        :func:`Rule.on_enter` method.

        :param flow: 
            :class:`Flow` which defines this state machine
        :returns: 
            newly created instance
        """
        state = State.objects.create(flow=flow, 
            current_node=flow.state_graph.root)
        flow.state_graph.root.data.rule.on_enter(state)
        return state