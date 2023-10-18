def __store_level_blocks(self, level_blocks):
        """!
        @brief Store level blocks if observing is enabled.

        @param[in] level_blocks (list): Created blocks on a new level.

        """
        self.__size += len(level_blocks)
        if self.__observe is True:
            self.__level_blocks.append(level_blocks)