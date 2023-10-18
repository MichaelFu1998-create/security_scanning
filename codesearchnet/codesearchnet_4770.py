def remove_entry(self, entry):
        """!
        @brief Remove clustering feature from the leaf node.
        
        @param[in] entry (cfentry): Clustering feature.
        
        """
                
        self.feature -= entry;
        self.entries.remove(entry);