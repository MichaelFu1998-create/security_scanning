def _process_exclude_dictionary(exclude_dictionary):
    """
    Based on values in the exclude_dictionary generate a list of term queries that
    will filter out unwanted results.
    """
    # not_properties will hold the generated term queries.
    not_properties = []
    for exclude_property in exclude_dictionary:
        exclude_values = exclude_dictionary[exclude_property]
        if not isinstance(exclude_values, list):
            exclude_values = [exclude_values]
        not_properties.extend([{"term": {exclude_property: exclude_value}} for exclude_value in exclude_values])

    # Returning a query segment with an empty list freaks out ElasticSearch,
    #   so just return an empty segment.
    if not not_properties:
        return {}

    return {
        "not": {
            "filter": {
                "or": not_properties
            }
        }
    }