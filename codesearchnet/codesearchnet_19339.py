def AdaBoost(L, K):
    """[Fig. 18.34]"""
    def train(dataset):
        examples, target = dataset.examples, dataset.target
        N = len(examples)
        epsilon = 1./(2*N)
        w = [1./N] * N
        h, z = [], []
        for k in range(K):
            h_k = L(dataset, w)
            h.append(h_k)
            error = sum(weight for example, weight in zip(examples, w)
                        if example[target] != h_k(example))
            # Avoid divide-by-0 from either 0% or 100% error rates:
            error = clip(error, epsilon, 1-epsilon)
            for j, example in enumerate(examples):
                if example[target] == h_k(example):
                    w[j] *= error / (1. - error)
            w = normalize(w)
            z.append(math.log((1. - error) / error))
        return WeightedMajority(h, z)
    return train