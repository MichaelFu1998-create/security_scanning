def rank_subgraph_by_node_filter(graph: BELGraph,
                                 node_predicates: Union[NodePredicate, Iterable[NodePredicate]],
                                 annotation: str = 'Subgraph',
                                 reverse: bool = True,
                                 ) -> List[Tuple[str, int]]:
    """Rank sub-graphs by which have the most nodes matching an given filter.

    A use case for this function would be to identify which subgraphs contain the most differentially expressed
    genes.

    >>> from pybel import from_pickle
    >>> from pybel.constants import GENE
    >>> from pybel_tools.integration import overlay_type_data
    >>> from pybel_tools.summary import rank_subgraph_by_node_filter
    >>> import pandas as pd
    >>> graph = from_pickle('~/dev/bms/aetionomy/alzheimers.gpickle')
    >>> df = pd.read_csv('~/dev/bananas/data/alzheimers_dgxp.csv', columns=['Gene', 'log2fc'])
    >>> data = {gene: log2fc for _, gene, log2fc in df.itertuples()}
    >>> overlay_type_data(graph, data, 'log2fc', GENE, 'HGNC', impute=0.0)
    >>> results = rank_subgraph_by_node_filter(graph, lambda g, n: 1.3 < abs(g[n]['log2fc']))
    """
    r1 = group_nodes_by_annotation_filtered(graph, node_predicates=node_predicates, annotation=annotation)
    r2 = count_dict_values(r1)
    # TODO use instead: r2.most_common()
    return sorted(r2.items(), key=itemgetter(1), reverse=reverse)