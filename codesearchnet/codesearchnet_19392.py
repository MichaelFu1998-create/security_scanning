def add_sequence(self, words):
        """Add each of the tuple words[i:i+n], using a sliding window.
        Prefix some copies of the empty word, '', to make the start work."""
        n = self.n
        words = ['',] * (n-1) + words
        for i in range(len(words)-n):
            self.add(tuple(words[i:i+n]))