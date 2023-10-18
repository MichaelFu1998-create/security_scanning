def cluster_lsun():
    "Not so applicable for this sample"
    start_centers = [[1.0, 3.5], [2.0, 0.5], [3.0, 3.0]]
    template_clustering(start_centers, FCPS_SAMPLES.SAMPLE_LSUN, criterion = splitting_type.BAYESIAN_INFORMATION_CRITERION)
    template_clustering(start_centers, FCPS_SAMPLES.SAMPLE_LSUN, criterion = splitting_type.MINIMUM_NOISELESS_DESCRIPTION_LENGTH)