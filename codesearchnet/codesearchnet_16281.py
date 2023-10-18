def build_this_graph(G, settings, dont_update_shas_of=None):
    """
    This is the master function that performs the building.

    Args:
        A graph (often a subgraph)
        The settings dictionary
        An optional list of files to not update the shas of
          (needed when building specific targets)

    Returns:
        0 if successful
        UN-success results in a fatal error so it will return 0 or nothing
    """
    verbose = settings["verbose"]
    quiet = settings["quiet"]
    force = settings["force"]
    recon = settings["recon"]
    parallel = settings["parallel"]
    error = settings["error"]
    sprint = settings["sprint"]

    if not dont_update_shas_of:
        dont_update_shas_of = []
    sprint("Checking that graph is directed acyclic", level="verbose")
    if not nx.is_directed_acyclic_graph(G):
        errmes = "Dependency resolution is impossible; "
        errmes += "graph is not directed and acyclic"
        errmes += "\nCheck the Sakefile\n"
        error(errmes)
        sys.exit(1)
    sprint("Dependency resolution is possible", level="verbose")
    in_mem_shas = take_shas_of_all_files(G, settings)
    from_store = {}
    if not os.path.isfile(".shastore"):
        write_shas_to_shastore(in_mem_shas)
        in_mem_shas = {}
        in_mem_shas['files'] = {}
    with io.open(".shastore", "r") as fh:
        shas_on_disk = fh.read()
    from_store = yaml.load(shas_on_disk)
    check_shastore_version(from_store, settings)
    if not from_store:
        write_shas_to_shastore(in_mem_shas)
        in_mem_shas = {}
        in_mem_shas['files'] = {}
        with io.open(".shastore", "r") as fh:
            shas_on_disk = fh.read()
        from_store = yaml.load(shas_on_disk)
    # parallel
    if parallel:
        for line in parallel_sort(G):
            line = sorted(line)
            out = "Checking if targets '{}' need to be run"
            sprint(out.format(", ".join(line)), level="verbose")
            to_build = []
            for item in line:
                if needs_to_run(G, item, in_mem_shas, from_store, settings):
                    to_build.append(item)
            if to_build:
                if recon:
                    if len(to_build) == 1:
                        out = "Would run target '{}'"
                        sprint(out.format(to_build[0]))
                    else:
                        out = "Would run targets '{}' in parallel"
                        sprint(out.format(", ".join(to_build)))
                    continue
                parallel_run_these(G, to_build, in_mem_shas, from_store,
                                   settings, dont_update_shas_of)
    # not parallel
    else:
        # still have to use parallel_sort to make
        # build order deterministic (by sorting targets)
        targets = []
        for line in parallel_sort(G):
            for item in sorted(line):
                targets.append(item)
        for target in targets:
            outstr = "Checking if target '{}' needs to be run"
            sprint(outstr.format(target), level="verbose")
            if needs_to_run(G, target, in_mem_shas, from_store, settings):
                if recon:
                    sprint("Would run target: {}".format(target))
                    continue
                run_the_target(G, target, settings)
                node_dict = get_the_node_dict(G, target)
                if "output" in node_dict:
                    for output in acts.get_all_outputs(node_dict):
                        if output not in dont_update_shas_of:
                            in_mem_shas['files'][output] = {"sha": get_sha(output,
                                                                           settings)}
                            write_shas_to_shastore(in_mem_shas)
                if "dependencies" in node_dict:
                    for dep in acts.get_all_dependencies(node_dict):
                        if dep not in dont_update_shas_of:
                            in_mem_shas['files'][dep] = {"sha": get_sha(dep,
                                                                        settings)}
                            write_shas_to_shastore(in_mem_shas)

    if recon:
        return 0
    in_mem_shas = take_shas_of_all_files(G, settings)
    if in_mem_shas:
        in_mem_shas = merge_from_store_and_in_mems(from_store, in_mem_shas,
                                                   dont_update_shas_of)
        write_shas_to_shastore(in_mem_shas)
    sprint("Done", color=True)
    return 0