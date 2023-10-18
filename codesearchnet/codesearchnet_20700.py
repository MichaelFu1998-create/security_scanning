def calculate_file_distances(dicom_files, field_weights=None,
                             dist_method_cls=None, **kwargs):
    """
    Calculates the DicomFileDistance between all files in dicom_files, using an
    weighted Levenshtein measure between all field names in field_weights and
    their corresponding weights.

    Parameters
    ----------
    dicom_files: iterable of str
        Dicom file paths

    field_weights: dict of str to float
        A dict with header field names to float scalar values, that
        indicate a distance measure ratio for the levenshtein distance
        averaging of all the header field names in it. e.g., {'PatientID': 1}

    dist_method_cls: DicomFileDistance class
        Distance method object to compare the files.
        If None, the default DicomFileDistance method using Levenshtein
        distance between the field_wieghts will be used.

    kwargs: DicomFileDistance instantiation named arguments
        Apart from the field_weitghts argument.

    Returns
    -------
    file_dists: np.ndarray or scipy.sparse.lil_matrix of shape NxN
        Levenshtein distances between each of the N items in dicom_files.
    """
    if dist_method_cls is None:
        dist_method = LevenshteinDicomFileDistance(field_weights)
    else:
        try:
            dist_method = dist_method_cls(field_weights=field_weights, **kwargs)
        except:
            log.exception('Could not instantiate {} object with field_weights '
                          'and {}'.format(dist_method_cls, kwargs))

    dist_dtype = np.float16
    n_files = len(dicom_files)

    try:
        file_dists = np.zeros((n_files, n_files), dtype=dist_dtype)
    except MemoryError as mee:
        import scipy.sparse
        file_dists = scipy.sparse.lil_matrix((n_files, n_files),
                                             dtype=dist_dtype)

    for idxi in range(n_files):
        dist_method.set_dicom_file1(dicom_files[idxi])

        for idxj in range(idxi+1, n_files):
            dist_method.set_dicom_file2(dicom_files[idxj])

            if idxi != idxj:
                file_dists[idxi, idxj] = dist_method.transform()

    return file_dists