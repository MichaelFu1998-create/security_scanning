def score_leaves(self) -> Set[BaseEntity]:
        """Calculate the score for all leaves.

        :return: The set of leaf nodes that were scored
        """
        leaves = set(self.iter_leaves())

        if not leaves:
            log.warning('no leaves.')
            return set()

        for leaf in leaves:
            self.graph.nodes[leaf][self.tag] = self.calculate_score(leaf)
            log.log(5, 'chomping %s', leaf)

        return leaves