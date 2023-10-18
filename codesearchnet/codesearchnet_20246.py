def auto_add(repo, autooptions, files):
    """
    Cleanup the paths and add
    """
    # Get the mappings and keys.
    mapping = { ".": "" }
    if (('import' in autooptions) and
        ('directory-mapping' in autooptions['import'])):
        mapping = autooptions['import']['directory-mapping']

    # Apply the longest prefix first...
    keys = mapping.keys()
    keys = sorted(keys, key=lambda k: len(k), reverse=True)

    count = 0
    params = []
    for f in files:

        # Find the destination
        relativepath = f
        for k in keys:
            v = mapping[k]
            if f.startswith(k + "/"):
                #print("Replacing ", k)
                relativepath = f.replace(k + "/", v)
                break

        # Now add to repository
        count += files_add(repo=repo,
                           args=[f],
                           targetdir=os.path.dirname(relativepath))

    return count