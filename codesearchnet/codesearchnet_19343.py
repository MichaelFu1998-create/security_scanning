def replicated_dataset(dataset, weights, n=None):
    "Copy dataset, replicating each example in proportion to its weight."
    n = n or len(dataset.examples)
    result = copy.copy(dataset)
    result.examples = weighted_replicate(dataset.examples, weights, n)
    return result