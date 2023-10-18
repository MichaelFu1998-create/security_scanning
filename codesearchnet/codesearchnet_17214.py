def export_namespaces(graph, namespaces, directory=None, cacheable=False):
    """Thinly wraps :func:`export_namespace` for an iterable of namespaces.

    :param pybel.BELGraph graph: A BEL graph
    :param iter[str] namespaces: An iterable of strings for the namespaces to process
    :param str directory: The path to the directory where to output the namespaces. Defaults to the current working
                      directory returned by :func:`os.getcwd`
    :param bool cacheable: Should the namespaces be cacheable? Defaults to ``False`` because, in general, this operation
                        will probably be used for evil, and users won't want to reload their entire cache after each
                        iteration of curation.
    """
    directory = os.getcwd() if directory is None else directory  # avoid making multiple calls to os.getcwd later
    for namespace in namespaces:
        export_namespace(graph, namespace, directory=directory, cacheable=cacheable)