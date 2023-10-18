def print_children(data_file, group='/'):
    """Print all the sub-groups in `group` and leaf-nodes children of `group`.

    Parameters:
        data_file (pytables HDF5 file object): the data file to print
        group (string): path name of the group to be printed.
            Default: '/', the root node.
    """
    base = data_file.get_node(group)
    print ('Groups in:\n  %s\n' % base)

    for node in base._f_walk_groups():
        if node is not base:
            print ('    %s' % node)

    print ('\nLeaf-nodes in %s:' % group)
    for node in base._v_leaves.itervalues():
        info = node.shape
        if len(info) == 0:
            info = node.read()
        print ('\t%s, %s' % (node.name, info))
        if len(node.title) > 0:
            print ('\t    %s' % node.title)