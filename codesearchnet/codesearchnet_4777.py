def insert_cluster(self, cluster):
        """!
        @brief Insert cluster that is represented as list of points where each point is represented by list of coordinates.
        @details Clustering feature is created for that cluster and inserted to the tree.
        
        @param[in] cluster (list): Cluster that is represented by list of points that should be inserted to the tree.
        
        """
        
        entry = cfentry(len(cluster), linear_sum(cluster), square_sum(cluster));
        self.insert(entry);