def find_module(self, fullname, path=None):
        """Find a module if its name starts with :code:`self.group` and is registered."""
        if not fullname.startswith(self._group_with_dot):
            return
        end_name = fullname[len(self._group_with_dot):]
        for entry_point in iter_entry_points(group=self.group, name=None):
            if entry_point.name == end_name:
                return self