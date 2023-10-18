def parses(self, words, S='S'):
        """Return a list of parses; words can be a list or string.
        >>> chart = Chart(E_NP_)
        >>> chart.parses('happy man', 'NP')
        [[0, 2, 'NP', [('Adj', 'happy'), [1, 2, 'NP', [('N', 'man')], []]], []]]
        """
        if isinstance(words, str):
            words = words.split()
        self.parse(words, S)
        # Return all the parses that span the whole input
        # 'span the whole input' => begin at 0, end at len(words)
        return [[i, j, S, found, []]
                for (i, j, lhs, found, expects) in self.chart[len(words)]
                # assert j == len(words)
                if i == 0 and lhs == S and expects == []]