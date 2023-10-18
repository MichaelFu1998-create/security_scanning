def loadGrammar(self, grammar, searchpaths=None):
        """load context-free grammar"""
        self.grammar = self._load(grammar, searchpaths=searchpaths)
        self.refs = {}
        for ref in self.grammar.getElementsByTagName("ref"):
            self.refs[ref.attributes["id"].value] = ref