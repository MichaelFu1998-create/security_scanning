def __draw_leaf_density(self):
        """!
        @brief Display densities by filling blocks by appropriate colors.

        """
        leafs = self.__directory.get_leafs()
        density_scale = leafs[-1].get_density()

        if density_scale == 0.0: density_scale = 1.0

        for block in leafs:
            alpha = 0.8 * block.get_density() / density_scale
            self.__draw_block(block, alpha)