def append_cluster(self, cluster, data=None, canvas=0, marker='.', markersize=None, color=None):
        """!
        @brief Appends cluster to canvas for drawing.
        
        @param[in] cluster (list): cluster that may consist of indexes of objects from the data or object itself.
        @param[in] data (list): If defines that each element of cluster is considered as a index of object from the data.
        @param[in] canvas (uint): Number of canvas that should be used for displaying cluster.
        @param[in] marker (string): Marker that is used for displaying objects from cluster on the canvas.
        @param[in] markersize (uint): Size of marker.
        @param[in] color (string): Color of marker.
        
        @return Returns index of cluster descriptor on the canvas.
        
        """
        
        if len(cluster) == 0:
            return
        
        if canvas > self.__number_canvases or canvas < 0:
            raise ValueError("Canvas index '%d' is out of range [0; %d]." % self.__number_canvases or canvas)
        
        if color is None:
            index_color = len(self.__canvas_clusters[canvas]) % len(color_list.TITLES)
            color = color_list.TITLES[index_color]
        
        added_canvas_descriptor = canvas_cluster_descr(cluster, data, marker, markersize, color)
        self.__canvas_clusters[canvas].append( added_canvas_descriptor )

        if data is None:
            dimension = len(cluster[0])
            if self.__canvas_dimensions[canvas] is None:
                self.__canvas_dimensions[canvas] = dimension
            elif self.__canvas_dimensions[canvas] != dimension:
                raise ValueError("Only clusters with the same dimension of objects can be displayed on canvas.")
                
        else:
            dimension = len(data[0])
            if self.__canvas_dimensions[canvas] is None:
                self.__canvas_dimensions[canvas] = dimension
            elif self.__canvas_dimensions[canvas] != dimension:
                raise ValueError("Only clusters with the same dimension of objects can be displayed on canvas.")

        if (dimension < 1) or (dimension > 3):
            raise ValueError("Only objects with size dimension 1 (1D plot), 2 (2D plot) or 3 (3D plot) "
                             "can be displayed. For multi-dimensional data use 'cluster_visualizer_multidim'.")
        
        if markersize is None:
            if (dimension == 1) or (dimension == 2):
                added_canvas_descriptor.markersize = self.__default_2d_marker_size
            elif dimension == 3:
                added_canvas_descriptor.markersize = self.__default_3d_marker_size
        
        return len(self.__canvas_clusters[canvas]) - 1