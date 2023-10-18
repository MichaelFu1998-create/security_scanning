def set_parent_path(self, value):
        """
        Set the parent path and the path from the new parent path.

        :param value: The path to the object's parent
        """

        self._parent_path = value
        self.path = value + r'/' + self.name
        self._update_childrens_parent_path()