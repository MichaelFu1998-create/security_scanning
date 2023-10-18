def largest_connected_component(volume):
    """Return the largest connected component of a 3D array.

    Parameters
    -----------
    volume: numpy.array
        3D boolean array.

    Returns
    --------
    volume: numpy.array
        3D boolean array with only one connected component.
    """
    # We use asarray to be able to work with masked arrays.
    volume = np.asarray(volume)
    labels, num_labels = scn.label(volume)
    if not num_labels:
        raise ValueError('No non-zero values: no connected components found.')

    if num_labels == 1:
        return volume.astype(np.bool)

    label_count = np.bincount(labels.ravel().astype(np.int))
    # discard the 0 label
    label_count[0] = 0
    return labels == label_count.argmax()