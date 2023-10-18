def print_attrs(data_file, node_name='/', which='user', compress=False):
    """Print the HDF5 attributes for `node_name`.

    Parameters:
        data_file (pytables HDF5 file object): the data file to print
        node_name (string): name of the path inside the file to be printed.
            Can be either a group or a leaf-node. Default: '/', the root node.
        which (string): Valid values are 'user' for user-defined attributes,
            'sys' for pytables-specific attributes and 'all' to print both
            groups of attributes. Default 'user'.
        compress (bool): if True displays at most a line for each attribute.
            Default False.
    """
    node = data_file.get_node(node_name)
    print ('List of attributes for:\n  %s\n' % node)
    for attr in node._v_attrs._f_list():
        print ('\t%s' % attr)
        attr_content = repr(node._v_attrs[attr])
        if compress:
            attr_content = attr_content.split('\n')[0]
        print ("\t    %s" % attr_content)