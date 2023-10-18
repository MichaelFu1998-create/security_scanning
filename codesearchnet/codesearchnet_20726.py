def add_meta_to_nii(nii_file, dicom_file, dcm_tags=''):
    """ Add slice duration and acquisition times to the headers of the nifit1 files in `nii_file`.
    It will add the repetition time of the DICOM file (field: {0x0018, 0x0080, DS, Repetition Time})
    to the NifTI file as well as any other tag in `dcm_tags`.
    All selected DICOM tags values are set in the `descrip` nifti header field.
    Note that this will modify the header content of `nii_file`.

    Parameters
    ----------
    nii_files: str
        Path to the NifTI file to modify.

    dicom_file: str
        Paths to the DICOM file from where to get the meta data.

    dcm_tags: list of str
        List of tags from the DICOM file to read and store in the nifti file.
    """
    # Load a dicom image
    dcmimage = dicom.read_file(dicom_file)

    # Load the nifti1 image
    image = nibabel.load(nii_file)

    # Check the we have a nifti1 format image
    if not isinstance(image, nibabel.nifti1.Nifti1Image):
        raise Exception(
            "Only Nifti1 image are supported not '{0}'.".format(
                type(image)))

    # check if dcm_tags is one string, if yes put it in a list:
    if isinstance(dcm_tags, str):
        dcm_tags = [dcm_tags]

    # Fill the nifti1 header
    header = image.get_header()

    # slice_duration: Time for 1 slice
    repetition_time = float(dcmimage[("0x0018", "0x0080")].value)
    header.set_dim_info(slice=2)
    nb_slices = header.get_n_slices()
    # Force round to 0 digit after coma. If more, nibabel completes to
    # 6 digits with random numbers...
    slice_duration = round(repetition_time / nb_slices, 0)
    header.set_slice_duration(slice_duration)

    # add free dicom fields
    if dcm_tags:
        content = ["{0}={1}".format(name, dcmimage[tag].value)
                   for name, tag in dcm_tags]
        free_field = numpy.array(";".join(content),
                                 dtype=header["descrip"].dtype)
        image.get_header()["descrip"] = free_field

    # Update the image header
    image.update_header()

    # Save the filled image
    nibabel.save(image, nii_file)