def rank_causalr_hypothesis(graph, node_to_regulation, regulator_node):
    """Test the regulator hypothesis of the given node on the input data using the algorithm.

    Note: this method returns both +/- signed hypotheses evaluated

    Algorithm:

    1. Calculate the shortest path between the regulator node and each node in observed_regulation
    2. Calculate the concordance of the causal network and the observed regulation when there is path
       between target node and regulator node

    :param networkx.DiGraph graph: A causal graph
    :param dict node_to_regulation: Nodes to score (1,-1,0)
    :return Dictionaries with hypothesis results (keys: score, correct, incorrect, ambiguous)
    :rtype: dict
    """
    upregulation_hypothesis = {
        'correct': 0,
        'incorrect': 0,
        'ambiguous': 0
    }
    downregulation_hypothesis = {
        'correct': 0,
        'incorrect': 0,
        'ambiguous': 0
    }

    targets = [
        node
        for node in node_to_regulation
        if node != regulator_node
    ]

    predicted_regulations = run_cna(graph, regulator_node, targets)  # + signed hypothesis

    for _, target_node, predicted_regulation in predicted_regulations:

        if (predicted_regulation is Effect.inhibition or predicted_regulation is Effect.activation) and (
                predicted_regulation.value == node_to_regulation[target_node]):
            upregulation_hypothesis['correct'] += 1
            downregulation_hypothesis['incorrect'] += 1

        elif predicted_regulation is Effect.ambiguous:
            upregulation_hypothesis['ambiguous'] += 1
            downregulation_hypothesis['ambiguous'] += 1

        elif predicted_regulation is Effect.no_effect:
            continue

        else:
            downregulation_hypothesis['correct'] += 1
            upregulation_hypothesis['incorrect'] += 1

    upregulation_hypothesis['score'] = upregulation_hypothesis['correct'] - upregulation_hypothesis['incorrect']
    downregulation_hypothesis['score'] = downregulation_hypothesis['correct'] - downregulation_hypothesis['incorrect']

    return upregulation_hypothesis, downregulation_hypothesis