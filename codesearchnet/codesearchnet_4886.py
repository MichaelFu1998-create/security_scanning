def __build_level(self, previous_level_blocks, level):
        """!
        @brief Build new level of directory.

        @param[in] previous_level_blocks (list): BANG-blocks on the previous level.
        @param[in] level (uint): Level number that should be built.

        @return (list) New block on the specified level.

        """
        current_level_blocks = []

        split_dimension = level % len(self.__data[0])
        cache_require = (level == self.__levels - 1)

        for block in previous_level_blocks:
            self.__split_block(block, split_dimension, cache_require, current_level_blocks)

        if cache_require:
            self.__leafs += current_level_blocks

        return current_level_blocks