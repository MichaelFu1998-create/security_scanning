def del_attr(self, name):
        """Implementation of attribute deletion

        ``del space.name`` by user script
        Called from ``StaticSpace.__delattr__``
        """
        if name in self.namespace:
            if name in self.cells:
                self.del_cells(name)
            elif name in self.spaces:
                self.del_space(name)
            elif name in self.refs:
                self.del_ref(name)
            else:
                raise RuntimeError("Must not happen")
        else:
            raise KeyError("'%s' not found in Space '%s'" % (name, self.name))