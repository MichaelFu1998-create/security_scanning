def instantiate(repo, name=None, filename=None):
    """
    Instantiate the generator and filename specification
    """

    default_transformers = repo.options.get('transformer', {})

    # If a name is specified, then lookup the options from dgit.json
    # if specfied. Otherwise it is initialized to an empty list of
    # files.
    transformers = {}
    if name is not None:
        # Handle the case generator is specified..
        if name in default_transformers:
            transformers = {
                name : default_transformers[name]
            }
        else:
            transformers = {
                name : {
                    'files': [],
                }
            }
    else:
        transformers = default_transformers

    #=========================================
    # Map the filename patterns to list of files
    #=========================================
    # Instantiate the files from the patterns specified
    input_matching_files = None
    if filename is not None:
        input_matching_files = repo.find_matching_files([filename])

    for t in transformers:
        for k in transformers[t]:
            if "files" not in k:
                continue
            if k == "files" and input_matching_files is not None:
                # Use the files specified on the command line..
                transformers[t][k] = input_matching_files
            else:
                # Try to match the specification
                if transformers[t][k] is None or len(transformers[t][k]) == 0:
                    transformers[t][k] = []
                else:
                    matching_files = repo.find_matching_files(transformers[t][k])
                    transformers[t][k] = matching_files

    return transformers