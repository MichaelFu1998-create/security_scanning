def convert_dcm2nii(input_dir, output_dir, filename):
    """ Call MRICron's `dcm2nii` to convert the DICOM files inside `input_dir`
    to Nifti and save the Nifti file in `output_dir` with a `filename` prefix.

    Parameters
    ----------
    input_dir: str
        Path to the folder that contains the DICOM files

    output_dir: str
        Path to the folder where to save the NifTI file

    filename: str
        Output file basename

    Returns
    -------
    filepaths: list of str
        List of file paths created in `output_dir`.
    """
    # a few checks before doing the job
    if not op.exists(input_dir):
        raise IOError('Expected an existing folder in {}.'.format(input_dir))

    if not op.exists(output_dir):
        raise IOError('Expected an existing output folder in {}.'.format(output_dir))

    # create a temporary folder for dcm2nii export
    tmpdir = tempfile.TemporaryDirectory(prefix='dcm2nii_')

    # call dcm2nii
    arguments = '-o "{}" -i y'.format(tmpdir.name)
    try:
        call_out = call_dcm2nii(input_dir, arguments)
    except:
        raise
    else:
        log.info('Converted "{}" to nifti.'.format(input_dir))

        # get the filenames of the files that dcm2nii produced
        filenames  = glob(op.join(tmpdir.name, '*.nii*'))

        # cleanup `filenames`, using only the post-processed (reoriented, cropped, etc.) images by dcm2nii
        cleaned_filenames = remove_dcm2nii_underprocessed(filenames)

        # copy files to the output_dir
        filepaths = []
        for srcpath in cleaned_filenames:
            dstpath = op.join(output_dir, filename)
            realpath = copy_w_plus(srcpath, dstpath)
            filepaths.append(realpath)

            # copy any other file produced by dcm2nii that is not a NifTI file, e.g., *.bvals, *.bvecs, etc.
            basename = op.basename(remove_ext(srcpath))
            aux_files = set(glob(op.join(tmpdir.name, '{}.*'     .format(basename)))) - \
                        set(glob(op.join(tmpdir.name, '{}.nii*'.format(basename))))
            for aux_file in aux_files:
                aux_dstpath = copy_w_ext(aux_file, output_dir, remove_ext(op.basename(realpath)))
                filepaths.append(aux_dstpath)

        return filepaths