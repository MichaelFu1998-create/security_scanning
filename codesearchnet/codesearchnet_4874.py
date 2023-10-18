def __draw_blocks(ax, blocks, pair):
        """!
        @brief Display BANG-blocks on specified figure.

        @param[in] ax (Axis): Axis where bang-blocks should be displayed.
        @param[in] blocks (list): List of blocks that should be displyed.
        @param[in] pair (tuple): Pair of coordinate index that should be displayed.

        """
        ax.grid(False)

        density_scale = blocks[-1].get_density()
        for block in blocks:
            bang_visualizer.__draw_block(ax, pair, block, density_scale)