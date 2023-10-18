def insert_entry(self, entry):
        """!
        @brief Insert new clustering feature to the leaf node.
        
        @param[in] entry (cfentry): Clustering feature.
        
        """
                              
        self.feature += entry;
        self.entries.append(entry);