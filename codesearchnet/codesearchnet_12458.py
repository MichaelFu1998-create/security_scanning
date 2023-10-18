def resolve_conflicts(inputs, outputs):
    """
    Checks for duplicate inputs and if there are any,
    remove one and set the output to the max of the two outputs
    Args:
        inputs (list<list<float>>): Array of input vectors
        outputs (list<list<float>>): Array of output vectors
    Returns:
        tuple<inputs, outputs>: The modified inputs and outputs
    """
    data = {}
    for inp, out in zip(inputs, outputs):
        tup = tuple(inp)
        if tup in data:
            data[tup].append(out)
        else:
            data[tup] = [out]

    inputs, outputs = [], []
    for inp, outs in data.items():
        inputs.append(list(inp))
        combined = [0] * len(outs[0])
        for i in range(len(combined)):
            combined[i] = max(j[i] for j in outs)
        outputs.append(combined)
    return inputs, outputs