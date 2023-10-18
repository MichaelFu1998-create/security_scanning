def clean_all(G, settings):
    """
    Removes all the output files from all targets. Takes
    the graph as the only argument

    Args:
        The networkx graph object
        The settings dictionary

    Returns:
        0 if successful
        1 if removing even one file failed
    """
    quiet = settings["quiet"]
    recon = settings["recon"]
    sprint = settings["sprint"]
    error = settings["error"]
    all_outputs = []
    for node in G.nodes(data=True):
        if "output" in node[1]:
            for item in get_all_outputs(node[1]):
                all_outputs.append(item)
    all_outputs.append(".shastore")
    retcode = 0
    for item in sorted(all_outputs):
        if os.path.isfile(item):
            if recon:
                sprint("Would remove file: {}".format(item))
                continue
            sprint("Attempting to remove file '{}'", level="verbose")
            try:
                os.remove(item)
                sprint("Removed file", level="verbose")
            except:
                errmes = "Error: file '{}' failed to be removed"
                error(errmes.format(item))
                retcode = 1
    if not retcode and not recon:
        sprint("All clean", color=True)
    return retcode