def NearestNeighborLearner(dataset, k=1):
    "k-NearestNeighbor: the k nearest neighbors vote."
    def predict(example):
        "Find the k closest, and have them vote for the best."
        best = heapq.nsmallest(k, ((dataset.distance(e, example), e)
                                   for e in dataset.examples))
        return mode(e[dataset.target] for (d, e) in best)
    return predict