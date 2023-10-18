def remove(self, line_data, root_type=None):
        """
        Marks line_data and all of its associated feature's 'line_status' as 'removed', does not actually remove the line_data from the data structure.
        The write function checks the 'line_status' when writing the gff file.
        Find the root parent of line_data of type root_type, remove all of its descendants.
        If the root parent has a parent with no children after the remove, remove the root parent's parent recursively.

        :param line_data:
        :param root_type:
        :return:
        """
        roots = [ld for ld in self.ancestors(line_data) if (root_type and ld['line_type'] == root_type) or (not root_type and not ld['parents'])] or [line_data]
        for root in roots:
            root['line_status'] = 'removed'
            root_descendants = self.descendants(root)
            for root_descendant in root_descendants:
                root_descendant['line_status'] = 'removed'
            root_ancestors = self.ancestors(root) # BFS, so we will process closer ancestors first
            for root_ancestor in root_ancestors:
                if len([ld for ld in root_ancestor['children'] if ld['line_status'] != 'removed']) == 0: # if all children of a root_ancestor is removed
                    # remove this root_ancestor
                    root_ancestor['line_status'] = 'removed'