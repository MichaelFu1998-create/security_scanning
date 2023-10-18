def score(self, word, docid):
        "Compute a score for this word on this docid."
        ## There are many options; here we take a very simple approach
        return (math.log(1 + self.index[word][docid])
                / math.log(1 + self.documents[docid].nwords))