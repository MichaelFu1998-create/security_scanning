def answer_display(self, s=''):
        """Helper method for displaying the answers so far.
        """
        padding = len(max(self.questions.keys(), key=len)) + 5
        for key in list(self.answers.keys()):
            s += '{:>{}} : {}\n'.format(key, padding, self.answers[key])
        return s