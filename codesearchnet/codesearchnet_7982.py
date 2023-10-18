def add_node(self, node):
        """Adds a `node` to the hash ring (including a number of replicas).
        """
        self.nodes.append(node)
        for x in xrange(self.replicas):
            ring_key = self.hash_method(b("%s:%d" % (node, x)))
            self.ring[ring_key] = node
            self.sorted_keys.append(ring_key)

        self.sorted_keys.sort()