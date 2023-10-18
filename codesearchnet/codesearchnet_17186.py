def to_html(graph: BELGraph) -> str:
    """Render the graph as an HTML string.

    Common usage may involve writing to a file like:

    >>> from pybel.examples import sialic_acid_graph
    >>> with open('html_output.html', 'w') as file:
    ...     print(to_html(sialic_acid_graph), file=file)
    """
    context = get_network_summary_dict(graph)
    summary_dict = graph.summary_dict()

    citation_years = context['citation_years']
    function_count = context['function_count']
    relation_count = context['relation_count']
    error_count = context['error_count']
    transformations_count = context['modifications_count']
    hub_data = context['hub_data']
    disease_data = context['disease_data']
    authors_count = context['authors_count']
    variants_count = context['variants_count']
    namespaces_count = context['namespaces_count']
    confidence_count = context['confidence_count']
    confidence_data = [
        (label, confidence_count.get(label, 0))
        for label in ('None', 'Very Low', 'Low', 'Medium', 'High', 'Very High')
    ]

    template = environment.get_template('index.html')
    return template.render(
        graph=graph,
        # Node Charts
        chart_1_data=prepare_c3(function_count, 'Node Count'),
        chart_6_data=prepare_c3(namespaces_count, 'Node Count'),
        chart_5_data=prepare_c3(variants_count, 'Node Count'),
        number_variants=sum(variants_count.values()),
        number_namespaces=len(namespaces_count),
        # Edge Charts
        chart_2_data=prepare_c3(relation_count, 'Edge Count'),
        chart_4_data=prepare_c3(transformations_count, 'Edge Count') if transformations_count else None,
        number_transformations=sum(transformations_count.values()),
        # Error Charts
        chart_3_data=prepare_c3(error_count, 'Error Type') if error_count else None,
        # Topology Charts
        chart_7_data=prepare_c3(hub_data, 'Degree'),
        chart_9_data=prepare_c3(disease_data, 'Degree') if disease_data else None,
        # Bibliometrics Charts
        chart_authors_count=prepare_c3(authors_count, 'Edges Contributed'),
        chart_10_data=prepare_c3_time_series(citation_years, 'Number of Articles') if citation_years else None,
        chart_confidence_count=prepare_c3(confidence_data, 'Edge Count'),
        summary_dict=summary_dict,
        # Everything else :)
        **context
    )