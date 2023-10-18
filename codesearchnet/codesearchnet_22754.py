def Split(cls, extended_path_mask):
        '''
        Splits the given path into their components: recursive, dirname, in_filters and out_filters

        :param str: extended_path_mask:
            The "extended path mask" to split

        :rtype: tuple(bool,bool,str,list(str),list(str))
        :returns:
            Returns the extended path 5 components:
            - The tree-recurse flag
            - The flat-recurse flag
            - The actual path
            - A list of masks to include
            - A list of masks to exclude
        '''
        import os.path
        r_tree_recurse = extended_path_mask[0] in '+-'
        r_flat_recurse = extended_path_mask[0] in '-'

        r_dirname, r_filters = os.path.split(extended_path_mask)
        if r_tree_recurse:
            r_dirname = r_dirname[1:]

        filters = r_filters.split(';')
        r_in_filters = [i for i in filters if not i.startswith('!')]
        r_out_filters = [i[1:] for i in filters if i.startswith('!')]

        return r_tree_recurse, r_flat_recurse, r_dirname, r_in_filters, r_out_filters