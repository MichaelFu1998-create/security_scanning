def _create_regs(self, state):
        """Creates a tuple of index pairs representing matched groups."""
        regs = [(state.start, state.string_position)]
        for group in range(self.re.groups):
            mark_index = 2 * group
            if mark_index + 1 < len(state.marks) \
                                    and state.marks[mark_index] is not None \
                                    and state.marks[mark_index + 1] is not None:
                regs.append((state.marks[mark_index], state.marks[mark_index + 1]))
            else:
                regs.append((-1, -1))
        return tuple(regs)