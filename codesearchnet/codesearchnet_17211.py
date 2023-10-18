def merge_namespaces(input_locations, output_path, namespace_name, namespace_keyword, namespace_domain, author_name,
                     citation_name, namespace_description=None, namespace_species=None, namespace_version=None,
                     namespace_query_url=None, namespace_created=None, author_contact=None, author_copyright=None,
                     citation_description=None, citation_url=None, citation_version=None, citation_date=None,
                     case_sensitive=True, delimiter='|', cacheable=True, functions=None, value_prefix='',
                     sort_key=None, check_keywords=True):
    """Merges namespaces from multiple locations to one.

    :param iter input_locations: An iterable of URLs or file paths pointing to BEL namespaces.
    :param str output_path: The path to the file to write the merged namespace
    :param str namespace_name: The namespace name
    :param str namespace_keyword: Preferred BEL Keyword, maximum length of 8
    :param str namespace_domain: One of: :data:`pybel.constants.NAMESPACE_DOMAIN_BIOPROCESS`,
                            :data:`pybel.constants.NAMESPACE_DOMAIN_CHEMICAL`,
                            :data:`pybel.constants.NAMESPACE_DOMAIN_GENE`, or
                            :data:`pybel.constants.NAMESPACE_DOMAIN_OTHER`
    :param str author_name: The namespace's authors
    :param str citation_name: The name of the citation
    :param str namespace_query_url: HTTP URL to query for details on namespace values (must be valid URL)
    :param str namespace_description: Namespace description
    :param str namespace_species: Comma-separated list of species taxonomy id's
    :param str namespace_version: Namespace version
    :param str namespace_created: Namespace public timestamp, ISO 8601 datetime
    :param str author_contact: Namespace author's contact info/email address
    :param str author_copyright: Namespace's copyright/license information
    :param str citation_description: Citation description
    :param str citation_url: URL to more citation information
    :param str citation_version: Citation version
    :param str citation_date: Citation publish timestamp, ISO 8601 Date
    :param bool case_sensitive: Should this config file be interpreted as case-sensitive?
    :param str delimiter: The delimiter between names and labels in this config file
    :param bool cacheable: Should this config file be cached?
    :param functions: The encoding for the elements in this namespace
    :type functions: iterable of characters
    :param str value_prefix: a prefix for each name
    :param sort_key: A function to sort the values with :func:`sorted`
    :param bool check_keywords: Should all the keywords be the same? Defaults to ``True``
    """
    results = get_merged_namespace_names(input_locations, check_keywords=check_keywords)

    with open(output_path, 'w') as file:
        write_namespace(
            namespace_name=namespace_name,
            namespace_keyword=namespace_keyword,
            namespace_domain=namespace_domain,
            author_name=author_name,
            citation_name=citation_name,
            values=results,
            namespace_species=namespace_species,
            namespace_description=namespace_description,
            namespace_query_url=namespace_query_url,
            namespace_version=namespace_version,
            namespace_created=namespace_created,
            author_contact=author_contact,
            author_copyright=author_copyright,
            citation_description=citation_description,
            citation_url=citation_url,
            citation_version=citation_version,
            citation_date=citation_date,
            case_sensitive=case_sensitive,
            delimiter=delimiter,
            cacheable=cacheable,
            functions=functions,
            value_prefix=value_prefix,
            sort_key=sort_key,
            file=file
        )