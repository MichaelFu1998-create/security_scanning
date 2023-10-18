def __create_directory(self):
        """!
        @brief Create BANG directory as a tree with separate storage for leafs.

        """

        min_corner, max_corner = data_corners(self.__data)
        data_block = spatial_block(max_corner, min_corner)

        cache_require = (self.__levels == 1)
        self.__root = bang_block(self.__data, 0, 0, data_block, cache_require)

        if cache_require:
            self.__leafs.append(self.__root)
            self.__store_level_blocks([self.__root])
        else:
            self.__build_directory_levels()