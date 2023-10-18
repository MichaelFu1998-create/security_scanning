def cluster_elongate():
    "Not so applicable for this sample"
    start_centers = [[1.0, 4.5], [3.1, 2.7]]
    template_clustering(start_centers, SIMPLE_SAMPLES.SAMPLE_ELONGATE, criterion = splitting_type.BAYESIAN_INFORMATION_CRITERION)
    template_clustering(start_centers, SIMPLE_SAMPLES.SAMPLE_ELONGATE, criterion = splitting_type.MINIMUM_NOISELESS_DESCRIPTION_LENGTH)