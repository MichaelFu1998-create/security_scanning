def group(self, *args):
        """Returns one or more subgroups of the match. Each argument is either a
        group index or a group name."""
        if len(args) == 0:
            args = (0,)
        grouplist = []
        for group in args:
            grouplist.append(self._get_slice(self._get_index(group), None))
        if len(grouplist) == 1:
            return grouplist[0]
        else:
            return tuple(grouplist)