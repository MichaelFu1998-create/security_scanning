def excerpt(self):
        """
        Property to display a useful excerpt representing the matches within the results
        """
        if "content" not in self._results_fields:
            return None

        match_phrases = [self._match_phrase]
        if six.PY2:
            separate_phrases = [
                phrase.decode('utf-8')
                for phrase in shlex.split(self._match_phrase.encode('utf-8'))
            ]
        else:
            separate_phrases = [
                phrase
                for phrase in shlex.split(self._match_phrase)
            ]
        if len(separate_phrases) > 1:
            match_phrases.extend(separate_phrases)
        else:
            match_phrases = separate_phrases

        matches = SearchResultProcessor.find_matches(
            SearchResultProcessor.strings_in_dictionary(self._results_fields["content"]),
            match_phrases,
            DESIRED_EXCERPT_LENGTH
        )
        excerpt_text = ELLIPSIS.join(matches)

        for match_word in match_phrases:
            excerpt_text = SearchResultProcessor.decorate_matches(excerpt_text, match_word)

        return excerpt_text