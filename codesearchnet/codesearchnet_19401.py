def decode(self, ciphertext):
        "Search for a decoding of the ciphertext."
        self.ciphertext = ciphertext
        problem = PermutationDecoderProblem(decoder=self)
        return search.best_first_tree_search(
            problem, lambda node: self.score(node.state))