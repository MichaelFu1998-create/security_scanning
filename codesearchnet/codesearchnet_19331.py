def PluralityLearner(dataset):
    """A very dumb algorithm: always pick the result that was most popular
    in the training data.  Makes a baseline for comparison."""
    most_popular = mode([e[dataset.target] for e in dataset.examples])
    def predict(example):
        "Always return same result: the most popular from the training set."
        return most_popular
    return predict