def present(self, results):
        "Present the results as a list."
        for (score, d) in results:
            doc = self.documents[d]
            print ("%5.2f|%25s | %s"
                   % (100 * score, doc.url, doc.title[:45].expandtabs()))