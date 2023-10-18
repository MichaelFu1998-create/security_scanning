def WeightedMajority(predictors, weights):
    "Return a predictor that takes a weighted vote."
    def predict(example):
        return weighted_mode((predictor(example) for predictor in predictors),
                             weights)
    return predict