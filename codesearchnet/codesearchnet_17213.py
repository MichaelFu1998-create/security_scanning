def export_namespace(graph, namespace, directory=None, cacheable=False):
    """Exports all names and missing names from the given namespace to its own BEL Namespace files in the given
    directory.

    Could be useful during quick and dirty curation, where planned namespace building is not a priority.

    :param pybel.BELGraph graph: A BEL graph
    :param str namespace: The namespace to process
    :param str directory: The path to the directory where to output the namespace. Defaults to the current working
                      directory returned by :func:`os.getcwd`
    :param bool cacheable: Should the namespace be cacheable? Defaults to ``False`` because, in general, this operation
                        will probably be used for evil, and users won't want to reload their entire cache after each
                        iteration of curation.
    """
    directory = os.getcwd() if directory is None else directory
    path = os.path.join(directory, '{}.belns'.format(namespace))

    with open(path, 'w') as file:
        log.info('Outputting to %s', path)
        right_names = get_names_by_namespace(graph, namespace)
        log.info('Graph has %d correct names in %s', len(right_names), namespace)
        wrong_names = get_incorrect_names_by_namespace(graph, namespace)
        log.info('Graph has %d incorrect names in %s', len(right_names), namespace)
        undefined_ns_names = get_undefined_namespace_names(graph, namespace)
        log.info('Graph has %d names in missing namespace %s', len(right_names), namespace)

        names = (right_names | wrong_names | undefined_ns_names)

        if 0 == len(names):
            log.warning('%s is empty', namespace)

        write_namespace(
            namespace_name=namespace,
            namespace_keyword=namespace,
            namespace_domain='Other',
            author_name=graph.authors,
            author_contact=graph.contact,
            citation_name=graph.name,
            values=names,
            cacheable=cacheable,
            file=file
        )