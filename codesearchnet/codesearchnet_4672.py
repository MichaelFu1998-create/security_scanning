def show(self, figure=None, invisible_axis=True, visible_grid=True, display=True, shift=None):
        """!
        @brief Shows clusters (visualize).
        
        @param[in] figure (fig): Defines requirement to use specified figure, if None - new figure is created for drawing clusters.
        @param[in] invisible_axis (bool): Defines visibility of axes on each canvas, if True - axes are invisible.
        @param[in] visible_grid (bool): Defines visibility of grid on each canvas, if True - grid is displayed.
        @param[in] display (bool): Defines requirement to display clusters on a stage, if True - clusters are displayed,
                    if False - plt.show() should be called by user."
        @param[in] shift (uint): Force canvas shift value - defines canvas index from which custers should be visualized.
        
        @return (fig) Figure where clusters are shown.
        
        """

        canvas_shift = shift
        if canvas_shift is None:
            if figure is not None:
                canvas_shift = len(figure.get_axes())
            else:
                canvas_shift = 0
            
        if figure is not None:
            cluster_figure = figure
        else:
            cluster_figure = plt.figure()
        
        maximum_cols = self.__size_row
        maximum_rows = math.ceil( (self.__number_canvases + canvas_shift) / maximum_cols)
        
        grid_spec = gridspec.GridSpec(maximum_rows, maximum_cols)

        for index_canvas in range(len(self.__canvas_clusters)):
            canvas_data = self.__canvas_clusters[index_canvas]
            if len(canvas_data) == 0:
                continue
        
            dimension = self.__canvas_dimensions[index_canvas]
            
            #ax = axes[real_index];
            if (dimension == 1) or (dimension == 2):
                ax = cluster_figure.add_subplot(grid_spec[index_canvas + canvas_shift])
            else:
                ax = cluster_figure.add_subplot(grid_spec[index_canvas + canvas_shift], projection='3d')
            
            if len(canvas_data) == 0:
                plt.setp(ax, visible=False)
            
            for cluster_descr in canvas_data:
                self.__draw_canvas_cluster(ax, dimension, cluster_descr)
                
                for attribute_descr in cluster_descr.attributes:
                    self.__draw_canvas_cluster(ax, dimension, attribute_descr)
            
            if invisible_axis is True:
                ax.xaxis.set_ticklabels([])
                ax.yaxis.set_ticklabels([])
                
                if (dimension == 3):
                    ax.zaxis.set_ticklabels([])
            
            if self.__canvas_titles[index_canvas] is not None:
                ax.set_title(self.__canvas_titles[index_canvas])
            
            ax.grid(visible_grid)
        
        if display is True:
            plt.show()
        
        return cluster_figure