def get_final_score(self) -> float:
        """Return the final score for the target node.

        :return: The final score for the target node
        """
        if not self.done_chomping():
            raise ValueError('algorithm has not yet completed')

        return self.graph.nodes[self.target_node][self.tag]