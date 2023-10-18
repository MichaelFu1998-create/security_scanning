def __build_directory_levels(self):
        """!
        @brief Build levels of direction if amount of level is greater than one.

        """

        previous_level_blocks = [ self.__root ]

        for level in range(1, self.__levels):
            previous_level_blocks = self.__build_level(previous_level_blocks, level)
            self.__store_level_blocks(previous_level_blocks)

        self.__leafs = sorted(self.__leafs, key=lambda block: block.get_density())