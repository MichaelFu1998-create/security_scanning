def hill_climbing(data, graph, **kwargs):
    """Hill Climbing optimization: a greedy exploration algorithm."""
    nodelist = list(data.columns)
    data = scale(data.values).astype('float32')
    tested_candidates = [nx.adj_matrix(graph, nodelist=nodelist, weight=None)]
    best_score = parallel_graph_evaluation(data, tested_candidates[0].todense(), ** kwargs)
    best_candidate = graph
    can_improve = True
    while can_improve:
        can_improve = False
        for (i, j) in best_candidate.edges():
            test_graph = deepcopy(best_candidate)
            test_graph.add_edge(j, i, weight=test_graph[i][j]['weight'])
            test_graph.remove_edge(i, j)
            tadjmat = nx.adj_matrix(test_graph, nodelist=nodelist, weight=None)
            if (nx.is_directed_acyclic_graph(test_graph) and not any([(tadjmat != cand).nnz ==
                                                                      0 for cand in tested_candidates])):
                tested_candidates.append(tadjmat)
                score = parallel_graph_evaluation(data, tadjmat.todense(), **kwargs)
                if score < best_score:
                    can_improve = True
                    best_candidate = test_graph
                    best_score = score
                    break
    return best_candidate