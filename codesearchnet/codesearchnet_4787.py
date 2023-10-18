def show_feature_destibution(self, data = None):
        """!
        @brief Shows feature distribution.
        @details Only features in 1D, 2D, 3D space can be visualized.
        
        @param[in] data (list): List of points that will be used for visualization, if it not specified than feature will be displayed only.
        
        """
        visualizer = cluster_visualizer();
        
        print("amount of nodes: ", self.__amount_nodes);
        
        if (data is not None):
            visualizer.append_cluster(data, marker = 'x');
        
        for level in range(0, self.height):
            level_nodes = self.get_level_nodes(level);
            
            centers = [ node.feature.get_centroid() for node in level_nodes ];
            visualizer.append_cluster(centers, None, markersize = (self.height - level + 1) * 5);
        
        visualizer.show();