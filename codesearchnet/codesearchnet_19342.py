def WeightedLearner(unweighted_learner):
    """Given a learner that takes just an unweighted dataset, return
    one that takes also a weight for each example. [p. 749 footnote 14]"""
    def train(dataset, weights):
        return unweighted_learner(replicated_dataset(dataset, weights))
    return train