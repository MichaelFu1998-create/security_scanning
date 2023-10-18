def set_encoding(self, encoding):
        """!
        @brief Change clusters encoding to specified type (index list, object list, labeling).
        
        @param[in] encoding (type_encoding): New type of clusters representation.
        
        """
        
        if(encoding == self.__type_representation):
            return;
        
        if (self.__type_representation == type_encoding.CLUSTER_INDEX_LABELING):
            if (encoding == type_encoding.CLUSTER_INDEX_LIST_SEPARATION):
                self.__clusters = self.__convert_label_to_index();
            
            else:
                self.__clusters = self.__convert_label_to_object();
        
        elif (self.__type_representation == type_encoding.CLUSTER_INDEX_LIST_SEPARATION):
            if (encoding == type_encoding.CLUSTER_INDEX_LABELING):
                self.__clusters = self.__convert_index_to_label();
            
            else:
                self.__clusters = self.__convert_index_to_object();
        
        else:
            if (encoding == type_encoding.CLUSTER_INDEX_LABELING):
                self.__clusters = self.__convert_object_to_label();
            
            else:
                self.__clusters = self.__convert_object_to_index();
        
        self.__type_representation = encoding;