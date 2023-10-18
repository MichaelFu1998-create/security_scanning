def _width(self):
        """For ``self.width``."""
        layout = self._instruction.get(GRID_LAYOUT)
        if layout is not None:
            width = layout.get(WIDTH)
            if width is not None:
                return width
        return self._instruction.number_of_consumed_meshes