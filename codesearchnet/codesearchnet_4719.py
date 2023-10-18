def cluster_two_diamonds():
    "Start with wrong number of clusters."
    start_centers = [[0.8, 0.2]]
    template_clustering(start_centers, FCPS_SAMPLES.SAMPLE_TWO_DIAMONDS, criterion = splitting_type.BAYESIAN_INFORMATION_CRITERION)
    template_clustering(start_centers, FCPS_SAMPLES.SAMPLE_TWO_DIAMONDS, criterion = splitting_type.MINIMUM_NOISELESS_DESCRIPTION_LENGTH)