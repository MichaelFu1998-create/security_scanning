def fit(self, X, y):
        """Fit CRF according to X, y

        Parameters
        ----------
        X : list of text
            each item is a text
        y: list
           each item is either a label (in multi class problem) or list of
           labels (in multi label problem)
        """
        trainer = pycrfsuite.Trainer(verbose=True)
        for xseq, yseq in zip(X, y):
            trainer.append(xseq, yseq)

        trainer.set_params(self.params)
        if self.filename:
            filename = self.filename
        else:
            filename = 'model.tmp'
        trainer.train(filename)
        tagger = pycrfsuite.Tagger()
        tagger.open(filename)
        self.estimator = tagger