def group_dicom_files(dicom_paths, hdr_field='PatientID'):
    """Group in a dictionary all the DICOM files in dicom_paths
    separated by the given `hdr_field` tag value.

    Parameters
    ----------
    dicom_paths: str
        Iterable of DICOM file paths.

    hdr_field: str
        Name of the DICOM tag whose values will be used as key for the group.

    Returns
    -------
    dicom_groups: dict of dicom_paths
    """
    dicom_groups = defaultdict(list)
    try:
        for dcm in dicom_paths:
            hdr = dicom.read_file(dcm)
            group_key = getattr(hdr, hdr_field)
            dicom_groups[group_key].append(dcm)
    except KeyError as ke:
        raise KeyError('Error reading field {} from file {}.'.format(hdr_field, dcm)) from ke

    return dicom_groups