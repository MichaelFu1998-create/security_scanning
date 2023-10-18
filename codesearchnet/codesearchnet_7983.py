def remove_node(self, node):
        """Removes `node` from the hash ring and its replicas.
        """
        self.nodes.remove(node)
        for x in xrange(self.replicas):
            ring_key = self.hash_method(b("%s:%d" % (node, x)))
            self.ring.pop(ring_key)
            self.sorted_keys.remove(ring_key)