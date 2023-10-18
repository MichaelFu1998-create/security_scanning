def groups(self, default=None):
        """Returns a tuple containing all the subgroups of the match. The
        default argument is used for groups that did not participate in the
        match (defaults to None)."""
        groups = []
        for indices in self.regs[1:]:
            if indices[0] >= 0:
                groups.append(self.string[indices[0]:indices[1]])
            else:
                groups.append(default)
        return tuple(groups)