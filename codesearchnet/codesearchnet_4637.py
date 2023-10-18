def show_ordering_diagram(analyser, amount_clusters = None):
        """!
        @brief Display cluster-ordering (reachability-plot) diagram.
        
        @param[in] analyser (ordering_analyser): cluster-ordering analyser whose ordering diagram should be displayed.
        @param[in] amount_clusters (uint): if it is not 'None' then it displays connectivity radius line that can used for allocation of specified amount of clusters
                    and colorize diagram by corresponding cluster colors.
        
        Example demonstrates general abilities of 'ordering_visualizer' class:
        @code
            # Display cluster-ordering diagram with connectivity radius is used for allocation of three clusters.
            ordering_visualizer.show_ordering_diagram(analyser, 3);
        
            # Display cluster-ordering diagram without radius.
            ordering_visualizer.show_ordering_diagram(analyser);
        @endcode
        
        """
        ordering = analyser.cluster_ordering
        axis = plt.subplot(111)
        
        if amount_clusters is not None:
            radius, borders = analyser.calculate_connvectivity_radius(amount_clusters)
        
            # divide into cluster groups to visualize by colors
            left_index_border = 0
            current_index_border = 0
            for index_border in range(len(borders)):
                right_index_border = borders[index_border]
                axis.bar(range(left_index_border, right_index_border), ordering[left_index_border:right_index_border], width = 1.0, color = color_list.TITLES[index_border])
                left_index_border = right_index_border
                current_index_border = index_border
            
            axis.bar(range(left_index_border, len(ordering)), ordering[left_index_border:len(ordering)], width = 1.0, color = color_list.TITLES[current_index_border + 1])
            
            plt.xlim([0, len(ordering)])
            
            plt.axhline(y = radius, linewidth = 2, color = 'black')
            plt.text(0, radius + radius * 0.03, " Radius:   " + str(round(radius, 4)) + ";\n Clusters: " + str(amount_clusters), color = 'b', fontsize = 10)
            
        else:
            axis.bar(range(0, len(ordering)), ordering[0:len(ordering)], width = 1.0, color = 'black')
            plt.xlim([0, len(ordering)])
        
        plt.show()