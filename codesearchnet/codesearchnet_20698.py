def group_dicom_files(dicom_file_paths, header_fields):
    """
    Gets a list of DICOM file absolute paths and returns a list of lists of
    DICOM file paths. Each group contains a set of DICOM files that have
    exactly the same headers.

    Parameters
    ----------
    dicom_file_paths: list of str
        List or set of DICOM file paths

    header_fields: list of str
        List of header field names to check on the comparisons of the DICOM files.

    Returns
    -------
    dict of DicomFileSets
        The key is one filepath representing the group (the first found).
    """
    dist = SimpleDicomFileDistance(field_weights=header_fields)

    path_list = dicom_file_paths.copy()

    path_groups = DefaultOrderedDict(DicomFileSet)

    while len(path_list) > 0:
        file_path1 = path_list.pop()
        file_subgroup = [file_path1]

        dist.set_dicom_file1(file_path1)
        j = len(path_list)-1
        while j >= 0:
            file_path2 = path_list[j]
            dist.set_dicom_file2(file_path2)

            if dist.transform():
                file_subgroup.append(file_path2)
                path_list.pop(j)

            j -= 1
        path_groups[file_path1].from_set(file_subgroup, check_if_dicoms=False)

    return path_groups