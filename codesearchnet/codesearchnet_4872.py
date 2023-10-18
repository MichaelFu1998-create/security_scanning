def show_blocks(directory):
        """!
        @brief Show BANG-blocks (leafs only) in data space.
        @details BANG-blocks represents grid that was used for clustering process.

        @param[in] directory (bang_directory): Directory that was created by BANG algorithm during clustering process.

        """

        dimension = len(directory.get_data()[0])

        amount_canvases = 1
        if dimension > 1:
            amount_canvases = int(dimension * (dimension - 1) / 2)

        figure = plt.figure()
        grid_spec = gridspec.GridSpec(1, amount_canvases)

        pairs = list(itertools.combinations(range(dimension), 2))
        if len(pairs) == 0: pairs = [(0, 0)]

        for index in range(amount_canvases):
            ax = figure.add_subplot(grid_spec[index])
            bang_visualizer.__draw_blocks(ax, directory.get_leafs(), pairs[index])
            bang_visualizer.__draw_two_dimension_data(ax, directory.get_data(), pairs[index])

        plt.show()