def get_clusters_representation(chromosome, count_clusters=None):
        """ Convert chromosome to cluster representation:
                chromosome : [0, 1, 1, 0, 2, 3, 3]
                clusters: [[0, 3], [1, 2], [4], [5, 6]]
        """

        if count_clusters is None:
            count_clusters = ga_math.calc_count_centers(chromosome)

        # Initialize empty clusters
        clusters = [[] for _ in range(count_clusters)]

        # Fill clusters with index of data
        for _idx_data in range(len(chromosome)):
            clusters[chromosome[_idx_data]].append(_idx_data)

        return clusters