def calc_centers(chromosomes, data, count_clusters=None):
        """!
        """

        if count_clusters is None:
            count_clusters = ga_math.calc_count_centers(chromosomes[0])

        # Initialize center
        centers = np.zeros(shape=(len(chromosomes), count_clusters, len(data[0])))

        for _idx_chromosome in range(len(chromosomes)):

            # Get count data in clusters
            count_data_in_cluster = np.zeros(count_clusters)

            # Next data point
            for _idx in range(len(chromosomes[_idx_chromosome])):

                cluster_num = chromosomes[_idx_chromosome][_idx]

                centers[_idx_chromosome][cluster_num] += data[_idx]
                count_data_in_cluster[cluster_num] += 1

            for _idx_cluster in range(count_clusters):
                if count_data_in_cluster[_idx_cluster] != 0:
                    centers[_idx_chromosome][_idx_cluster] /= count_data_in_cluster[_idx_cluster]

        return centers