def cluster_sample3():
    "Start with wrong number of clusters."
    start_centers = [[0.2, 0.1], [4.0, 1.0]]
    template_clustering(start_centers, SIMPLE_SAMPLES.SAMPLE_SIMPLE3, criterion = splitting_type.BAYESIAN_INFORMATION_CRITERION)
    template_clustering(start_centers, SIMPLE_SAMPLES.SAMPLE_SIMPLE3, criterion = splitting_type.MINIMUM_NOISELESS_DESCRIPTION_LENGTH)