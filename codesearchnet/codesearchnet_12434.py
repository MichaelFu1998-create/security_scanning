def add(self, *args, **kwargs):
        """Add a Question instance to the questions dict. Each key points
        to a list of Question instances with that key. Use the `question`
        kwarg to pass a Question instance if you want, or pass in the same
        args you would pass to instantiate a question.
        """
        if 'question' in kwargs and isinstance(kwargs['question'], Question):
            question = kwargs['question']
        else:
            question = Question(*args, **kwargs)
        self.questions.setdefault(question.key, []).append(question)
        return question