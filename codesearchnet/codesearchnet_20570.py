def get_unique_field_values(dcm_file_list, field_name):
    """Return a set of unique field values from a list of DICOM files

    Parameters
    ----------
    dcm_file_list: iterable of DICOM file paths

    field_name: str
     Name of the field from where to get each value

    Returns
    -------
    Set of field values
    """
    field_values = set()

    for dcm in dcm_file_list:
        field_values.add(str(DicomFile(dcm).get_attributes(field_name)))

    return field_values