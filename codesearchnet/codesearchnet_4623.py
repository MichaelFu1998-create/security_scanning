def __fill_tree(self, data_list, payload_list):
        """!
        @brief Fill KD-tree by specified data and create point comparator in line with data type.

        @param[in] data_list (array_like): Data points that should be inserted to the tree.
        @param[in] payload_list (array_like): Data point payloads that follows data points inserted to the tree.

        """
        if data_list is None or len(data_list) == 0:
            return # Just return from here, tree can be filled by insert method later

        if payload_list is None:
            # Case when payload is not specified.
            for index in range(0, len(data_list)):
                self.insert(data_list[index], None)
        else:
            # Case when payload is specified.
            for index in range(0, len(data_list)):
                self.insert(data_list[index], payload_list[index])

        self.__point_comparator = self.__create_point_comparator(type(self.__root.data))