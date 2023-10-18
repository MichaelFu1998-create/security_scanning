def run_cna(graph, root, targets, relationship_dict=None):
    """ Returns the effect from the root to the target nodes represented as {-1,1}

    :param pybel.BELGraph graph: A BEL graph
    :param BaseEntity root: The root node
    :param iter targets: The targets nodes
    :param dict relationship_dict: dictionary with relationship effects
    :return list[tuple]:
    """
    causal_effects = []

    relationship_dict = causal_effect_dict if relationship_dict is None else relationship_dict

    for target in targets:
        try:
            shortest_paths = nx.all_shortest_paths(graph, source=root, target=target)

            effects_in_path = set()

            for shortest_path in shortest_paths:
                effects_in_path.add(get_path_effect(graph, shortest_path, relationship_dict))

            if len(effects_in_path) == 1:
                causal_effects.append((root, target, next(iter(effects_in_path))))  # Append the only predicted effect

            elif Effect.activation in effects_in_path and Effect.inhibition in effects_in_path:
                causal_effects.append((root, target, Effect.ambiguous))

            elif Effect.activation in effects_in_path and Effect.inhibition not in effects_in_path:
                causal_effects.append((root, target, Effect.activation))

            elif Effect.inhibition in effects_in_path and Effect.activation not in effects_in_path:
                causal_effects.append((root, target, Effect.inhibition))

            else:
                log.warning('Exception in set: {}.'.format(effects_in_path))

        except nx.NetworkXNoPath:
            log.warning('No shortest path between: {} and {}.'.format(root, target))

    return causal_effects