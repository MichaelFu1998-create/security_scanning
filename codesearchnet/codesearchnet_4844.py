def __allocate_clusters(self):
        """!
        @brief Performs cluster analysis using formed CLIQUE blocks.

        """
        for cell in self.__cells:
            if cell.visited is False:
                self.__expand_cluster(cell)