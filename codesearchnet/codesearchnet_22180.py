def prune_list(self):
        """Returns a list of nodes that would be removed if prune were called
        on this element.
        """
        targets = self.descendents_root()
        try:
            targets.remove(self.graph.root)
        except ValueError:
            # root wasn't in the target list, no problem
            pass

        targets.append(self)
        return targets