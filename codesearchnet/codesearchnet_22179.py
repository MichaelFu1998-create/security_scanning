def prune(self):
        """Removes the node and all descendents without looping back past the
        root.  Note this does not remove the associated data objects.

        :returns:
            list of :class:`BaseDataNode` subclassers associated with the
            removed ``Node`` objects.
        """
        targets = self.descendents_root()
        try:
            targets.remove(self.graph.root)
        except ValueError:
            # root wasn't in the target list, no problem
            pass

        results = [n.data for n in targets]
        results.append(self.data)
        for node in targets:
            node.delete()

        for parent in self.parents.all():
            parent.children.remove(self)

        self.delete()
        return results