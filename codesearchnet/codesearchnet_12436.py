def next_question(self):
        """Returns the next `Question` in the questionnaire, or `None` if there
        are no questions left. Returns first question for whose key there is no
        answer and for which condition is satisfied, or for which there is no
        condition.
        """
        for key, questions in self.questions.items():
            if key in self.answers:
                continue
            for question in questions:
                if self.check_condition(question._condition):
                    return question
        return None