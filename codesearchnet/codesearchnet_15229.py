def load_module(self, fullname):
        """Load a module if its name starts with :code:`self.group` and is registered."""
        if fullname in sys.modules:
            return sys.modules[fullname]
        end_name = fullname[len(self._group_with_dot):]
        for entry_point in iter_entry_points(group=self.group, name=end_name):
            mod = entry_point.load()
            sys.modules[fullname] = mod
            return mod