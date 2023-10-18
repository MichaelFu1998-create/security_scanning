def __read_answer_from_line(self, index_point, line):
        """!
        @brief Read information about point from the specific line and place it to cluster or noise in line with that
                information.

        @param[in] index_point (uint): Index point that should be placed to cluster or noise.
        @param[in] line (string): Line where information about point should be read.

        """

        if line[0] == 'n':
            self.__noise.append(index_point)
        else:
            index_cluster = int(line)
            if index_cluster >= len(self.__clusters):
                self.__clusters.append([index_point])
            else:
                self.__clusters[index_cluster].append(index_point)