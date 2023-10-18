def licenses_from_tree(self, tree):
        """
        Traverse conjunctions and disjunctions like trees and return a
        set of all licenses in it as nodes.
        """
        # FIXME: this is unordered!
        licenses = set()
        self.licenses_from_tree_helper(tree, licenses)
        return licenses