def parallel_run_these(G, list_of_targets, in_mem_shas, from_store,
                       settings, dont_update_shas_of):
    """
    The parallel equivalent of "run_this_target()"
    It receives a list of targets to execute in parallel.
    Unlike "run_this_target()" it has to update the shas
    (in memory and in the store) within the function.
    This is because one of the targets may fail but many can
    succeed, and those outputs need to be updated

    Args:
        G
        A graph
        A list of targets that we need to build in parallel
        The dictionary containing the in-memory sha store
        The dictionary containing the contents of the .shastore file
        The settings dictionary
        A list of outputs to not update shas of
    """
    verbose = settings["verbose"]
    quiet = settings["quiet"]
    error = settings["error"]
    sprint = settings["sprint"]

    if len(list_of_targets) == 1:
        target = list_of_targets[0]
        sprint("Going to run target '{}' serially".format(target),
               level="verbose")
        run_the_target(G, target, settings)
        node_dict = get_the_node_dict(G, target)
        if "output" in node_dict:
            for output in acts.get_all_outputs(node_dict):
                if output not in dont_update_shas_of:
                    in_mem_shas['files'][output] = {"sha": get_sha(output,
                                                                   settings)}
                    in_mem_shas[output] = get_sha(output, settings)
                    write_shas_to_shastore(in_mem_shas)
        if "dependencies" in node_dict:
            for dep in acts.get_all_dependencies(node_dict):
                if dep not in dont_update_shas_of:
                    in_mem_shas['files'][dep] = {"sha": get_sha(dep, settings)}
                    write_shas_to_shastore(in_mem_shas)
        return True
    a_failure_occurred = False
    out = "Going to run these targets '{}' in parallel"
    sprint(out.format(", ".join(list_of_targets)))
    info = [(target, get_the_node_dict(G, target))
              for target in list_of_targets]
    commands = [item[1]['formula'].rstrip() for item in info]
    if not quiet:
        procs = [Popen(command, shell=True) for command in commands]
    else:
        procs = [Popen(command, shell=True, stdout=PIPE, stderr=PIPE)
                   for command in commands]
    for index, process in enumerate(procs):
        if process.wait():
            error("Target '{}' failed!".format(info[index][0]))
            a_failure_occurred = True
        else:
            if "output" in info[index][1]:
                for output in acts.get_all_outputs(info[index][1]):
                    if output not in dont_update_shas_of:
                        in_mem_shas['files'][output] = {"sha": get_sha(output,
                                                                       settings)}
                        write_shas_to_shastore(in_mem_shas)
            if "dependencies" in info[index][1]:
                for dep in acts.get_all_dependencies(info[index][1]):
                    if dep not in dont_update_shas_of:
                        in_mem_shas['files'][dep] = {"sha": get_sha(dep, settings)}
                        write_shas_to_shastore(in_mem_shas)
    if a_failure_occurred:
        error("A command failed to run")
        sys.exit(1)
    return True