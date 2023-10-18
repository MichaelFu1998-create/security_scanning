def cluster_sample2():
    "Start with wrong number of clusters."
    start_centers = [[3.5, 4.8], [2.6, 2.5]]
    template_clustering(start_centers, SIMPLE_SAMPLES.SAMPLE_SIMPLE2, criterion = splitting_type.BAYESIAN_INFORMATION_CRITERION)
    template_clustering(start_centers, SIMPLE_SAMPLES.SAMPLE_SIMPLE2, criterion = splitting_type.MINIMUM_NOISELESS_DESCRIPTION_LENGTH)