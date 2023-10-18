def calc_intent(self, query):
        """
        Tests all the intents against the query and returns
        match data of the best intent

        Args:
            query (str): Input sentence to test against intents
        Returns:
            MatchData: Best intent match
        """
        matches = self.calc_intents(query)
        if len(matches) == 0:
            return MatchData('', '')
        best_match = max(matches, key=lambda x: x.conf)
        best_matches = (match for match in matches if match.conf == best_match.conf)
        return min(best_matches, key=lambda x: sum(map(len, x.matches.values())))