def add(repo, args, targetdir,
        execute=False, generator=False,
        includes=[], script=False,
        source=None):
    """
    Add files to the repository by explicitly specifying them or by
    specifying a pattern over files accessed during execution of an
    executable.

    Parameters
    ----------

    repo: Repository

    args: files or command line
         (a) If simply adding files, then the list of files that must
         be added (including any additional arguments to be passed to
         git
         (b) If files to be added are an output of a command line, then
         args is the command lined
    targetdir: Target directory to store the files
    execute: Args are not files to be added but scripts that must be run.
    includes: patterns used to select files to
    script: Is this a script?
    generator: Is this a generator
    source: Link to the original source of the data

    """

    # Gather the files...
    if not execute:
        files = add_files(args=args,
                          targetdir=targetdir,
                          source=source,
                          script=script,
                          generator=generator)
    else:
        files = run_executable(repo, args, includes)

    if files is None or len(files) == 0:
        return repo


    # Update the repo package but with only those that have changed.

    filtered_files = []
    package = repo.package
    for h in files:
        found = False
        for i, r in  enumerate(package['resources']):
            if h['relativepath'] == r['relativepath']:
                found = True
                if h['sha256'] == r['sha256']:
                    change = False
                    for attr in ['source']:
                        if h[attr] != r[attr]:
                            r[attr] = h[attr]
                            change = True
                    if change:
                        filtered_files.append(h)
                    continue
                else:
                    filtered_files.append(h)
                    package['resources'][i] = h
                break
        if not found:
            filtered_files.append(h)
            package['resources'].append(h)

    if len(filtered_files) == 0:
        return 0

    # Copy the files
    repo.manager.add_files(repo, filtered_files)

    # Write to disk...
    rootdir = repo.rootdir
    with cd(rootdir):
        datapath = "datapackage.json"
        with open(datapath, 'w') as fd:
            fd.write(json.dumps(package, indent=4))

    return len(filtered_files)