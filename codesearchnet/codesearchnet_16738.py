def del_cells(self, name):
        """Implementation of cells deletion

        ``del space.name`` where name is a cells, or
        ``del space.cells['name']``
        """
        if name in self.cells:
            cells = self.cells[name]
            self.cells.del_item(name)
            self.inherit()
            self.model.spacegraph.update_subspaces(self)

        elif name in self.dynamic_spaces:
            cells = self.dynamic_spaces.pop(name)
            self.dynamic_spaces.set_update()

        else:
            raise KeyError("Cells '%s' does not exist" % name)

        NullImpl(cells)