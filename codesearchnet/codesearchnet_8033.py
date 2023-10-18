def get_suggestions(self, prefix, fuzzy = False, num = 10, with_scores = False, with_payloads=False):
        """
        Get a list of suggestions from the AutoCompleter, for a given prefix

        ### Parameters:
        - **prefix**: the prefix we are searching. **Must be valid ascii or utf-8**
        - **fuzzy**: If set to true, the prefix search is done in fuzzy mode. 
            **NOTE**: Running fuzzy searches on short (<3 letters) prefixes can be very slow, and even scan the entire index.
        - **with_scores**: if set to true, we also return the (refactored) score of each suggestion. 
          This is normally not needed, and is NOT the original score inserted into the index
        - **with_payloads**: Return suggestion payloads
        - **num**: The maximum number of results we return. Note that we might return less. The algorithm trims irrelevant suggestions.
        
        Returns a list of Suggestion objects. If with_scores was False, the score of all suggestions is 1.
        """

        args = [AutoCompleter.SUGGET_COMMAND, self.key, prefix, 'MAX', num]
        if fuzzy:
            args.append(AutoCompleter.FUZZY)
        if with_scores:
            args.append(AutoCompleter.WITHSCORES)
        if with_payloads:
            args.append(AutoCompleter.WITHPAYLOADS)

        ret = self.redis.execute_command(*args)
        results = []
        if not ret:
            return results

        parser = SuggestionParser(with_scores, with_payloads, ret)
        return [s for s in parser]