def __create_grid_spec(self, amount_axis, max_row_size):
        """!
        @brief Create grid specification for figure to place canvases.

        @param[in] amount_axis (uint): Amount of canvases that should be organized by the created grid specification.
        @param[in] max_row_size (max_row_size): Maximum number of canvases on one row.

        @return (gridspec.GridSpec) Grid specification to place canvases on figure.

        """
        row_size = amount_axis
        if row_size > max_row_size:
            row_size = max_row_size

        col_size = math.ceil(amount_axis / row_size)
        return gridspec.GridSpec(col_size, row_size)