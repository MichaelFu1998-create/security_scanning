def go_back(self, n=1):
        """Move `n` questions back in the questionnaire by removing the last `n`
        answers.
        """
        if not self.can_go_back:
            return
        N = max(len(self.answers)-abs(n), 0)
        self.answers = OrderedDict(islice(self.answers.items(), N))