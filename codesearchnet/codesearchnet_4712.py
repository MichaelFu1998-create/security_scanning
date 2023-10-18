def cluster_sample1():
    "Start with wrong number of clusters."
    start_centers = [[3.7, 5.5]]
    template_clustering(start_centers, SIMPLE_SAMPLES.SAMPLE_SIMPLE1, criterion = splitting_type.BAYESIAN_INFORMATION_CRITERION)
    template_clustering(start_centers, SIMPLE_SAMPLES.SAMPLE_SIMPLE1, criterion = splitting_type.MINIMUM_NOISELESS_DESCRIPTION_LENGTH)