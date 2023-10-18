def __merge_by_centroid_link(self):
        """!
        @brief Merges the most similar clusters in line with centroid link type.
        
        """
        
        minimum_centroid_distance = float('Inf');
        indexes = None;
        
        for index1 in range(0, len(self.__centers)):
            for index2 in range(index1 + 1, len(self.__centers)):
                distance = euclidean_distance_square(self.__centers[index1], self.__centers[index2]);
                if (distance < minimum_centroid_distance):
                    minimum_centroid_distance = distance;
                    indexes = [index1, index2];
        
        self.__clusters[indexes[0]] += self.__clusters[indexes[1]];
        self.__centers[indexes[0]] = self.__calculate_center(self.__clusters[indexes[0]]);
         
        self.__clusters.pop(indexes[1]);   # remove merged cluster.
        self.__centers.pop(indexes[1]);