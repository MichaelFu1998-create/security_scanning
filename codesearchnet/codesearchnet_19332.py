def NaiveBayesLearner(dataset):
    """Just count how many times each value of each input attribute
    occurs, conditional on the target value. Count the different
    target values too."""

    targetvals = dataset.values[dataset.target]
    target_dist = CountingProbDist(targetvals)
    attr_dists = dict(((gv, attr), CountingProbDist(dataset.values[attr]))
                      for gv in targetvals
                      for attr in dataset.inputs)
    for example in dataset.examples:
        targetval = example[dataset.target]
        target_dist.add(targetval)
        for attr in dataset.inputs:
            attr_dists[targetval, attr].add(example[attr])

    def predict(example):
        """Predict the target value for example. Consider each possible value,
        and pick the most likely by looking at each attribute independently."""
        def class_probability(targetval):
            return (target_dist[targetval]
                    * product(attr_dists[targetval, attr][example[attr]]
                              for attr in dataset.inputs))
        return argmax(targetvals, class_probability)

    return predict