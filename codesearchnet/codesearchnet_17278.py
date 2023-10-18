def run_with_graph_transformation(self) -> Iterable[BELGraph]:
        """Calculate scores for all leaves until there are none, removes edges until there are, and repeats until
        all nodes have been scored. Also, yields the current graph at every step so you can make a cool animation
        of how the graph changes throughout the course of the algorithm

        :return: An iterable of BEL graphs
        """
        yield self.get_remaining_graph()
        while not self.done_chomping():
            while not list(self.iter_leaves()):
                self.remove_random_edge()
                yield self.get_remaining_graph()
            self.score_leaves()
            yield self.get_remaining_graph()