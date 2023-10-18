def iter_nodes(self, key):
        """Given a string key it returns the nodes as a generator that can hold the key.
        """
        if len(self.ring) == 0:
            yield None, None
        node, pos = self.get_node_pos(key)
        for k in self.sorted_keys[pos:]:
            yield k, self.ring[k]