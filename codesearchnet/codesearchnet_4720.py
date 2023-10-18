def cluster_hepta():
    "Start with wrong number of clusters."
    start_centers = [[0.0, 0.0, 0.0], [3.0, 0.0, 0.0], [-2.0, 0.0, 0.0], [0.0, 3.0, 0.0], [0.0, -3.0, 0.0], [0.0, 0.0, 2.5]]
    template_clustering(start_centers, FCPS_SAMPLES.SAMPLE_HEPTA, criterion = splitting_type.BAYESIAN_INFORMATION_CRITERION)
    template_clustering(start_centers, FCPS_SAMPLES.SAMPLE_HEPTA, criterion = splitting_type.MINIMUM_NOISELESS_DESCRIPTION_LENGTH)