def visualize(G, settings, filename="dependencies", no_graphviz=False):
    """
    Uses networkX to draw a graphviz dot file either (a) calls the
    graphviz command "dot" to turn it into a SVG and remove the
    dotfile (default), or (b) if no_graphviz is True, just output
    the graphviz dot file

    Args:
        a NetworkX DiGraph
        the settings dictionary
        a filename (a default is provided
        a flag indicating whether graphviz should *not* be called

    Returns:
        0 if everything worked
        will cause fatal error on failure
    """
    error = settings["error"]
    if no_graphviz:
        write_dot_file(G, filename)
        return 0
    write_dot_file(G, "tempdot")
    renderer = "svg"
    if re.search("\.jpg$", filename, re.IGNORECASE):
        renderer = "jpg"
    elif re.search("\.jpeg$", filename, re.IGNORECASE):
        renderer = "jpg"
    elif re.search("\.svg$", filename, re.IGNORECASE):
        renderer = "svg"
    elif re.search("\.png$", filename, re.IGNORECASE):
        renderer = "png"
    elif re.search("\.gif$", filename, re.IGNORECASE):
        renderer = "gif"
    elif re.search("\.ps$", filename, re.IGNORECASE):
        renderer = "ps"
    elif re.search("\.pdf$", filename, re.IGNORECASE):
        renderer = "pdf"
    else:
        renderer = "svg"
        filename += ".svg"
    command = "dot -T{} tempdot -o {}".format(renderer, filename)
    p = Popen(command, shell=True)
    p.communicate()
    if p.returncode:
        errmes = "Either graphviz is not installed, or its not on PATH"
        os.remove("tempdot")
        error(errmes)
        sys.exit(1)
    os.remove("tempdot")
    return 0