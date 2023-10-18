def calc_intents(self, query):
        """
        Tests all the intents against the query and returns
        data on how well each one matched against the query

        Args:
            query (str): Input sentence to test against intents
        Returns:
            list<MatchData>: List of intent matches
        See calc_intent() for a description of the returned MatchData
        """
        if self.must_train:
            self.train()
        intents = {} if self.train_thread and self.train_thread.is_alive() else {
            i.name: i for i in self.intents.calc_intents(query, self.entities)
        }
        sent = tokenize(query)
        for perfect_match in self.padaos.calc_intents(query):
            name = perfect_match['name']
            intents[name] = MatchData(name, sent, matches=perfect_match['entities'], conf=1.0)
        return list(intents.values())