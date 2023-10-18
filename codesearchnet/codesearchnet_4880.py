def __draw_clusters(self):
        """!
        @brief Display clusters and outliers using different colors.

        """
        data = self.__directory.get_data()
        for index_cluster in range(len(self.__clusters)):
            color = color_list.get_color(index_cluster)
            self.__draw_cluster(data, self.__clusters[index_cluster], color, '.')

        self.__draw_cluster(self.__directory.get_data(), self.__noise, 'gray', 'x')