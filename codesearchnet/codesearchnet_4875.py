def __draw_block(ax, pair, block, density_scale):
        """!
        @brief Display BANG-block on the specified ax.

        @param[in] ax (Axis): Axis where block should be displayed.
        @param[in] pair (tuple): Pair of coordinate index that should be displayed.
        @param[in] block (bang_block): BANG-block that should be displayed.
        @param[in] density_scale (double): Max density to display density of the block by appropriate tone.

        """
        max_corner, min_corner = bang_visualizer.__get_rectangle_description(block, pair)

        belong_cluster = block.get_cluster() is not None

        if density_scale != 0.0:
            density_scale = bang_visualizer.__maximum_density_alpha * block.get_density() / density_scale

        face_color = matplotlib.colors.to_rgba('blue', alpha=density_scale)
        edge_color = matplotlib.colors.to_rgba('black', alpha=1.0)

        rect = patches.Rectangle(min_corner, max_corner[0] - min_corner[0], max_corner[1] - min_corner[1],
                                 fill=belong_cluster,
                                 facecolor=face_color,
                                 edgecolor=edge_color,
                                 linewidth=0.5)
        ax.add_patch(rect)