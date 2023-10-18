def as_list(self):
        """Returns a list of strings describing the full paths and patterns
        along with the name of the urls.  Example:

        .. code-block::python
            >>> u = URLTree()
            >>> u.as_list()
            [
                'admin/',
                'admin/$, name=index',
                'admin/login/$, name=login',
            ]
        """
        result = []
        for child in self.children:
            self._depth_traversal(child, result)

        return result