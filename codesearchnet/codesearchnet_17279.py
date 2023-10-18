def done_chomping(self) -> bool:
        """Determines if the algorithm is complete by checking if the target node of this analysis has been scored
        yet. Because the algorithm removes edges when it gets stuck until it is un-stuck, it is always guaranteed to
        finish.

        :return: Is the algorithm done running?
        """
        return self.tag in self.graph.nodes[self.target_node]