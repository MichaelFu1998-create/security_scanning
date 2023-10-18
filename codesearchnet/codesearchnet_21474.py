def path(self, include_root=False):
        """
        Returns a canonical path to this element, relative to the root node.

        :param include_root: If ``True``, include the root node in the path. Defaults to ``False``.
        """
        path = '%s[%d]' % (self.tagname, self.index or 0)
        p = self.parent
        while p is not None:
            if p.parent or include_root:
                path = '%s[%d]/%s' % (p.tagname, p.index or 0, path)
            p = p.parent
        return path