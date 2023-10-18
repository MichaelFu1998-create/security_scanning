def information_content(values):
    "Number of bits to represent the probability distribution in values."
    probabilities = normalize(removeall(0, values))
    return sum(-p * log2(p) for p in probabilities)