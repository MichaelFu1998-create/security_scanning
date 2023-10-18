def __extract_features(self):
        """!
        @brief Extracts features from CF-tree cluster.
        
        """
        
        self.__features = [];
        
        if (len(self.__tree.leafes) == 1):
            # parameters are too general, copy all entries
            for entry in self.__tree.leafes[0].entries:
                self.__features.append(entry);

        else:
            # copy all leaf clustering features
            for node in self.__tree.leafes:
                self.__features.append(node.feature);