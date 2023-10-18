def import_funcs(self, module):
        """Create a cells from a module."""
        # Outside formulas only
        newcells = self._impl.new_cells_from_module(module)
        return get_interfaces(newcells)