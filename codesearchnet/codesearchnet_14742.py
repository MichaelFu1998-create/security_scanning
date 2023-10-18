def parse(self, text):
        """
        
        Arguments:
        - `self`:
        - `text`:
        """

        results = list()
        
        for oneline in text.split('\n'):
            self._tagger.stdin.write(oneline+'\n')
            while True:
                r = self._tagger.stdout.readline()[:-1]
                if not r:
                    break
                results.append(tuple(r.split('\t')))
        return results