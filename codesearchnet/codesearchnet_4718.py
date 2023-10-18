def cluster_target():
    "Not so applicable for this sample"
    start_centers = [[0.2, 0.2], [0.0, -2.0], [3.0, -3.0], [3.0, 3.0], [-3.0, 3.0], [-3.0, -3.0]]
    template_clustering(start_centers, FCPS_SAMPLES.SAMPLE_TARGET, criterion = splitting_type.BAYESIAN_INFORMATION_CRITERION)
    template_clustering(start_centers, FCPS_SAMPLES.SAMPLE_TARGET, criterion = splitting_type.MINIMUM_NOISELESS_DESCRIPTION_LENGTH)