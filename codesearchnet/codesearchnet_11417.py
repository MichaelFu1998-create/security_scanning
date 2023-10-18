def _process_facet_terms(facet_terms):
    """ We have a list of terms with which we return facets """
    elastic_facets = {}
    for facet in facet_terms:
        facet_term = {"field": facet}
        if facet_terms[facet]:
            for facet_option in facet_terms[facet]:
                facet_term[facet_option] = facet_terms[facet][facet_option]

        elastic_facets[facet] = {
            "terms": facet_term
        }

    return elastic_facets