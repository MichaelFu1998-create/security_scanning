def get_merged_namespace_names(locations, check_keywords=True):
    """Loads many namespaces and combines their names.

    :param iter[str] locations: An iterable of URLs or file paths pointing to BEL namespaces.
    :param bool check_keywords: Should all the keywords be the same? Defaults to ``True``
    :return: A dictionary of {names: labels}
    :rtype: dict[str, str]

    Example Usage

    >>> from pybel.resources import write_namespace
    >>> from pybel_tools.definition_utils import export_namespace, get_merged_namespace_names
    >>> graph = ...
    >>> original_ns_url = ...
    >>> export_namespace(graph, 'MBS') # Outputs in current directory to MBS.belns
    >>> value_dict = get_merged_namespace_names([original_ns_url, 'MBS.belns'])
    >>> with open('merged_namespace.belns', 'w') as f:
    >>> ...  write_namespace('MyBrokenNamespace', 'MBS', 'Other', 'Charles Hoyt', 'PyBEL Citation', value_dict, file=f)
    """
    resources = {location: get_bel_resource(location) for location in locations}

    if check_keywords:
        resource_keywords = set(config['Namespace']['Keyword'] for config in resources.values())
        if 1 != len(resource_keywords):
            raise ValueError('Tried merging namespaces with different keywords: {}'.format(resource_keywords))

    result = {}
    for resource in resources:
        result.update(resource['Values'])
    return result