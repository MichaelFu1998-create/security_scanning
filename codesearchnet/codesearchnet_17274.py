def get_random_edge(self):
        """This function should be run when there are no leaves, but there are still unscored nodes. It will introduce
        a probabilistic element to the algorithm, where some edges are disregarded randomly to eventually get a score
        for the network. This means that the score can be averaged over many runs for a given graph, and a better
        data structure will have to be later developed that doesn't destroy the graph (instead, annotates which edges
        have been disregarded, later)

           1. get all un-scored
           2. rank by in-degree
           3. weighted probability over all in-edges where lower in-degree means higher probability
           4. pick randomly which edge

        :return: A random in-edge to the lowest in/out degree ratio node. This is a 3-tuple of (node, node, key)
        :rtype: tuple
        """
        nodes = [
            (n, self.in_out_ratio(n))
            for n in self.unscored_nodes_iter()
            if n != self.target_node
        ]

        node, deg = min(nodes, key=itemgetter(1))
        log.log(5, 'checking %s (in/out ratio: %.3f)', node, deg)

        possible_edges = self.graph.in_edges(node, keys=True)
        log.log(5, 'possible edges: %s', possible_edges)

        edge_to_remove = random.choice(possible_edges)
        log.log(5, 'chose: %s', edge_to_remove)

        return edge_to_remove