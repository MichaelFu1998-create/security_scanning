def show_dendrogram(dendrogram):
        """!
        @brief Display dendrogram of BANG-blocks.

        @param[in] dendrogram (list): List representation of dendrogram of BANG-blocks.

        @see bang.get_dendrogram()

        """
        plt.figure()
        axis = plt.subplot(1, 1, 1)

        current_position = 0
        for index_cluster in range(len(dendrogram)):
            densities = [ block.get_density() for block in dendrogram[index_cluster] ]
            xrange = range(current_position, current_position + len(densities))

            axis.bar(xrange, densities, 1.0, linewidth=0.0, color=color_list.get_color(index_cluster))

            current_position += len(densities)

        axis.set_ylabel("density")
        axis.set_xlabel("block")
        axis.xaxis.set_ticklabels([])

        plt.xlim([-0.5, current_position - 0.5])
        plt.show()