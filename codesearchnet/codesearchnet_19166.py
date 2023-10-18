def verify_words(self):
        """Verify the fields source, imagery_used and comment of the changeset
        for some suspect words.
        """
        if self.comment:
            if find_words(self.comment, self.suspect_words, self.excluded_words):
                self.label_suspicious('suspect_word')

        if self.source:
            for word in self.illegal_sources:
                if word in self.source.lower():
                    self.label_suspicious('suspect_word')
                    break

        if self.imagery_used:
            for word in self.illegal_sources:
                if word in self.imagery_used.lower():
                    self.label_suspicious('suspect_word')
                    break

        self.suspicion_reasons = list(set(self.suspicion_reasons))