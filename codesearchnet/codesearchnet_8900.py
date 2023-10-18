def copy(self):
        """Returns a deep copy of itself."""
        net = QueueNetwork(None)
        net.g = self.g.copy()
        net.max_agents = copy.deepcopy(self.max_agents)
        net.nV = copy.deepcopy(self.nV)
        net.nE = copy.deepcopy(self.nE)
        net.num_agents = copy.deepcopy(self.num_agents)
        net.num_events = copy.deepcopy(self.num_events)
        net._t = copy.deepcopy(self._t)
        net._initialized = copy.deepcopy(self._initialized)
        net._prev_edge = copy.deepcopy(self._prev_edge)
        net._blocking = copy.deepcopy(self._blocking)
        net.colors = copy.deepcopy(self.colors)
        net.out_edges = copy.deepcopy(self.out_edges)
        net.in_edges = copy.deepcopy(self.in_edges)
        net.edge2queue = copy.deepcopy(self.edge2queue)
        net._route_probs = copy.deepcopy(self._route_probs)

        if net._initialized:
            keys = [q._key() for q in net.edge2queue if q._time < np.infty]
            net._fancy_heap = PriorityQueue(keys, net.nE)

        return net