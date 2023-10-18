def query(self, query_text, n=10):
        """Return a list of n (score, docid) pairs for the best matches.
        Also handle the special syntax for 'learn: command'."""
        if query_text.startswith("learn:"):
            doctext = os.popen(query_text[len("learn:"):], 'r').read()
            self.index_document(doctext, query_text)
            return []
        qwords = [w for w in words(query_text) if w not in self.stopwords]
        shortest = argmin(qwords, lambda w: len(self.index[w]))
        docs = self.index[shortest]
        results = [(sum([self.score(w, d) for w in qwords]), d) for d in docs]
        results.sort(); results.reverse()
        return results[:n]