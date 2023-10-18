def large_clusters_mask(volume, min_cluster_size):
    """ Return as mask for `volume` that includes only areas where
    the connected components have a size bigger than `min_cluster_size`
    in number of voxels.

    Parameters
    -----------
    volume: numpy.array
        3D boolean array.

    min_cluster_size: int
        Minimum size in voxels that the connected component must have.

    Returns
    --------
    volume: numpy.array
        3D int array with a mask excluding small connected components.
    """
    labels, num_labels = scn.label(volume)

    labels_to_keep = set([i for i in range(num_labels)
                         if np.sum(labels == i) >= min_cluster_size])

    clusters_mask = np.zeros_like(volume, dtype=int)
    for l in range(num_labels):
        if l in labels_to_keep:
            clusters_mask[labels == l] = 1

    return clusters_mask