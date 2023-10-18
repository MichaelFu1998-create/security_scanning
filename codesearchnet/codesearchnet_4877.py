def __increment_block(self):
        """!
        @brief Increment BANG block safely by updating block index, level and level block.

        """
        self.__current_block += 1
        if self.__current_block >= len(self.__level_blocks):
            self.__current_block = 0
            self.__current_level += 1

            if self.__current_level < self.__directory.get_height():
                self.__level_blocks = self.__directory.get_level(self.__current_level)