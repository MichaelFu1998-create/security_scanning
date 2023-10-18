def ask(self, error=None):
        """Asks the next question in the questionnaire and returns the answer,
        unless user goes back.
        """
        q = self.next_question
        if q is None:
            return

        try:
            answer = q.prompter(self.get_prompt(q, error), *q.prompter_args, **q.prompter_kwargs)
        except QuestionnaireGoBack as e:
            steps = e.args[0] if e.args else 1
            if steps == 0:
                self.ask()  # user can redo current question even if `can_go_back` is `False`
                return
            self.go_back(steps)
        else:
            if q._validate:
                error = q._validate(answer)
                if error:
                    self.ask(error)
                    return
            if q._transform:
                answer = q._transform(answer)
            self.answers[q.key] = answer
            return answer