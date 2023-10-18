def __draw_block(self, block, block_alpha=0.0):
        """!
        @brief Display single BANG block on axis.

        @param[in] block (bang_block): BANG block that should be displayed.
        @param[in] block_alpha (double): Transparency level - value of alpha.

        """
        max_corner, min_corner = block.get_spatial_block().get_corners()

        face_color = matplotlib.colors.to_rgba('blue', alpha=block_alpha)
        edge_color = matplotlib.colors.to_rgba('black', alpha=1.0)

        rect = patches.Rectangle(min_corner, max_corner[0] - min_corner[0], max_corner[1] - min_corner[1],
                                 fill=True,
                                 facecolor=face_color,
                                 edgecolor=edge_color,
                                 linewidth=0.5)
        self.__ax.add_patch(rect)