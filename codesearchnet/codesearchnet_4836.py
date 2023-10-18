def show_grid(cells, data):
        """!
        @brief Show CLIQUE blocks as a grid in data space.
        @details Each block contains points and according to this density is displayed. CLIQUE grid helps to visualize
                  grid that was used for clustering process.

        @param[in] cells (list): List of cells that is produced by CLIQUE algorithm.
        @param[in] data (array_like): Input data that was used for clustering process.

        """
        dimension = cells[0].dimensions

        amount_canvases = 1
        if dimension > 1:
            amount_canvases = int(dimension * (dimension - 1) / 2)

        figure = plt.figure()
        grid_spec = gridspec.GridSpec(1, amount_canvases)

        pairs = list(itertools.combinations(range(dimension), 2))
        if len(pairs) == 0: pairs = [(0, 0)]

        for index in range(amount_canvases):
            ax = figure.add_subplot(grid_spec[index])
            clique_visualizer.__draw_cells(ax, cells, pairs[index])
            clique_visualizer.__draw_two_dimension_data(ax, data, pairs[index])

        plt.show()