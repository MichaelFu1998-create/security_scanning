def annotate_metadata_data(repo, task, patterns=["*"], size=0):
    """
    Update metadata with the content of the files
    """

    mgr = plugins_get_mgr() 
    keys = mgr.search('representation')['representation']
    representations = [mgr.get_by_key('representation', k) for k in keys]

    matching_files = repo.find_matching_files(patterns)
    package = repo.package
    rootdir = repo.rootdir
    files = package['resources']
    for f in files:
        relativepath = f['relativepath']
        if relativepath in matching_files:
            path = os.path.join(rootdir, relativepath)
            if task == 'preview':
                print("Adding preview for ", relativepath)
                f['content'] = open(path).read()[:size]
            elif task == 'schema':
                for r in representations: 
                    if r.can_process(path): 
                        print("Adding schema for ", path)
                        f['schema'] = r.get_schema(path)
                        break