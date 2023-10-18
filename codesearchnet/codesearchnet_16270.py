def take_shas_of_all_files(G, settings):
    """
    Takes sha1 hash of all dependencies and outputs of all targets

    Args:
        The graph we are going to build
        The settings dictionary

    Returns:
        A dictionary where the keys are the filenames and the
        value is the sha1 hash
    """
    global ERROR_FN
    sprint = settings["sprint"]
    error = settings["error"]
    ERROR_FN = error
    sha_dict = {}
    all_files = []
    for target in G.nodes(data=True):
        sprint("About to take shas of files in target '{}'".format(target[0]),
               level="verbose")
        if 'dependencies' in target[1]:
            sprint("It has dependencies", level="verbose")
            deplist = []
            for dep in target[1]['dependencies']:
                glist = glob.glob(dep)
                if glist:
                    for oneglob in glist:
                        deplist.append(oneglob)
                else:
                    deplist.append(dep)
            target[1]['dependencies'] = list(deplist)
            for dep in target[1]['dependencies']:
                sprint("  - {}".format(dep), level="verbose")
                all_files.append(dep)
        if 'output' in target[1]:
            sprint("It has outputs", level="verbose")
            for out in acts.get_all_outputs(target[1]):
                sprint("  - {}".format(out), level="verbose")
                all_files.append(out)
    if len(all_files):
        sha_dict['files'] = {}
        # check if files exist and de-dupe
        extant_files = []
        for item in all_files:
            if item not in extant_files and os.path.isfile(item):
                extant_files.append(item)
        pool = Pool()
        results = pool.map(get_sha, extant_files)
        pool.close()
        pool.join()
        for fn, sha in zip(extant_files, results):
            sha_dict['files'][fn] = {'sha': sha}
        return sha_dict
    sprint("No dependencies", level="verbose")