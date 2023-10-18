def get_centres(chromosomes, data, count_clusters):
        """!
        """

        centres = ga_math.calc_centers(chromosomes, data, count_clusters)

        return centres