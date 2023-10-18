def EnsembleLearner(learners):
    """Given a list of learning algorithms, have them vote."""
    def train(dataset):
        predictors = [learner(dataset) for learner in learners]
        def predict(example):
            return mode(predictor(example) for predictor in predictors)
        return predict
    return train