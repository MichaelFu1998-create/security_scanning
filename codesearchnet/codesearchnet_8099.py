def project(*descs, root_file=None):
    """
    Make a new project, using recursion and alias resolution.

    Use this function in preference to calling Project() directly.
    """
    load.ROOT_FILE = root_file

    desc = merge.merge(merge.DEFAULT_PROJECT, *descs)
    path = desc.get('path', '')

    if root_file:
        project_path = os.path.dirname(root_file)
        if path:
            path += ':' + project_path
        else:
            path = project_path

    with load.extender(path):
        desc = recurse.recurse(desc)

    project = construct.construct(**desc)
    project.desc = desc
    return project