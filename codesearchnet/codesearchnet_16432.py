def cluster(node):
    """Get cluster and nodes info."""
    cluster_client = PolyaxonClient().cluster
    if node:
        try:
            node_config = cluster_client.get_node(node)
        except (PolyaxonHTTPError, PolyaxonShouldExitError, PolyaxonClientException) as e:
            Printer.print_error('Could not load node `{}` info.'.format(node))
            Printer.print_error('Error message `{}`.'.format(e))
            sys.exit(1)
        get_node_info(node_config)
    else:
        try:
            cluster_config = cluster_client.get_cluster()
        except (PolyaxonHTTPError, PolyaxonShouldExitError, PolyaxonClientException) as e:
            Printer.print_error('Could not load cluster info.')
            Printer.print_error('Error message `{}`.'.format(e))
            sys.exit(1)
        get_cluster_info(cluster_config)