def top(self, n):
        "Return (count, obs) tuples for the n most frequent observations."
        return heapq.nlargest(n, [(v, k) for (k, v) in self.dictionary.items()])