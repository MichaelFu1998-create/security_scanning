def __merge_similar_clusters(self):
        """!
        @brief Merges the most similar clusters in line with link type.
        
        """
        
        if (self.__similarity == type_link.AVERAGE_LINK):
            self.__merge_by_average_link();
        
        elif (self.__similarity == type_link.CENTROID_LINK):
            self.__merge_by_centroid_link();
        
        elif (self.__similarity == type_link.COMPLETE_LINK):
            self.__merge_by_complete_link();
        
        elif (self.__similarity == type_link.SINGLE_LINK):
            self.__merge_by_signle_link();
        
        else:
            raise NameError('Not supported similarity is used');